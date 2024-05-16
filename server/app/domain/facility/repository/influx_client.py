import csv
import gzip
from collections import defaultdict
from datetime import datetime, timedelta
import time
from http.client import HTTPException
from io import StringIO, BytesIO

import numpy as np
import pandas as pd
from fastapi import UploadFile, File
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS, WriteOptions, ASYNCHRONOUS, PointSettings
from influxdb_client.client.write.dataframe_serializer import data_frame_to_list_of_points

from typing import List, Any
from loguru import logger
from starlette.responses import JSONResponse
from urllib3.exceptions import NewConnectionError

from app.domain.facility.service.facility_function import get_measurement_code
from app.domain.facility.service.facility_query import field_by_time_query, execute_query, info_measurements_query, \
    info_field_query, TGLife_query
from app.domain.section.model.section_data import SectionData
from app.domain.section.service.batch_service import save_section_data
from config import settings

# from influxapi.schemas import InfluxWaveRecord

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InfluxNotAvailableException(Exception):
    STATUS_CODE = 503
    DESCRIPTION = "InfluxDB API client is not available"


class BucketNotFoundException(Exception):
    STATUS_CODE = 404
    DESCRIPTION = "Bucket not found"


class DataNotFoundException(Exception):
    STATUS_CODE = 404
    DESCRIPTION = "Data not found"


class BadQueryException(Exception):
    STATUS_CODE = 400
    DESCRIPTION = "Bad query"


class InfluxGTRClient:

    # constructor
    def __init__(self, url: str, token: str, org: str, bucket_name: str) -> None:
        self.bucket_name = bucket_name
        self.client = InfluxDBClient(url=url, token=token, org=org, timeout=60000)

    # write
    def write_csv(self, files: List[UploadFile] = File(...), batch_size=900) -> []:
        total_time = time.time()
        # create write api
        write_api = self.client.write_api(write_options=
        WriteOptions(
            batch_size=batch_size,
            write_type=ASYNCHRONOUS
        ))

        # create bucket if not exist
        self.createBucket(self.client)

        response = []
        cnt = 0
        for file in files:
            # start time
            start_time = time.time()

            # await self.write_not_df(write_api, file, batch_size)
            res = self.write_df(write_api, file, batch_size)
            if res['status'] == 'success':
                cnt += 1
            response.append(res)

            # end time
            print('time: ', time.time() - start_time)
            print('-----------------------')

        write_api.close()
        count = {'count': cnt}
        print('total time: ', time.time() - total_time)

        return count, response

    def read_data(self, conditions: List[SectionData]) -> []:
        start_time = time.time()
        result_df = pd.DataFrame()

        # conditions length == 1
        if len(conditions) == 1:
            query = field_by_time_query(
                b=self.bucket_name, facility=conditions[0].facility, field=conditions[0].parameter,
                start_date=conditions[0].startTime, end_date=conditions[0].endTime)
            try:
                result_df = execute_query(self.client, query)
                result_df.rename(
                    columns={f'{conditions[0].parameter}': f'{conditions[0].facility}_{conditions[0].parameter}'},
                    inplace=True)
            except Exception as e:
                raise HTTPException(500, str(e))

        # conditions length > 1
        if len(conditions) > 1:
            for condition in conditions:
                query = field_by_time_query(
                    b=self.bucket_name, facility=condition.facility, field=condition.parameter,
                    start_date=condition.startTime, end_date=condition.endTime)

                try:
                    result_df['Time'] = execute_query(self.client, query)[['Time']]
                except Exception as e:
                    print(e)

                try:
                    result_df[f'{condition.facility}_{condition.parameter}'] = execute_query(self.client, query)[
                        [condition.parameter]]
                    # df_list.append(df)
                except Exception as e:
                    raise HTTPException(500, str(e))

        print('time: ', time.time() - start_time)
        return ["step", result_df]

    def read_info(self):
        answer_measurements = execute_query(self.client, info_measurements_query(b=self.bucket_name))

        facilities = defaultdict(list)
        for measurement in answer_measurements['_value']:
            answer_fields = self.client.query_api().query_data_frame(
                info_field_query(b=self.bucket_name, measurement=measurement))

            fields = [field for field in answer_fields['_value']]
            facilities[measurement] = fields

        return {'result': dict(facilities)}

    def read_TG_data(self, facility: object, tg_life_num: str, start_date: object, end_date: object) -> object:
        start_time = time.time()
        result_df = pd.DataFrame()

        # conditions length == 1
        # def TGLife_query(b: str, facility: str, tg_life: str, start_date: str, end_date: str):
        statistics_list = ["AVG", "MAX", "MIN", "STDDEV"]
        answer_df = pd.DataFrame()
        for idx, statistics in enumerate(statistics_list):
            count_flag = False
            if idx == len(statistics_list) - 1:
                count_flag = True

            query = TGLife_query(b=self.bucket_name, facility=facility, tg_life_num=tg_life_num,
                                 start_date=start_date, end_date=end_date, type=statistics, count=count_flag)
            try:
                result_df = execute_query(self.client, query)

                result_df.rename(
                    columns={f'P.TG{tg_life_num}I[A]': f'{statistics}-P.TG{tg_life_num}I[A]',
                             f'P.TG{tg_life_num}Pwr[kW]': f'{statistics}-P.TG{tg_life_num}Pwr[kW]',
                             f'P.TG{tg_life_num}V[V]': f'{statistics}-P.TG{tg_life_num}V[V]'},
                    inplace=True)

                if idx == len(statistics_list) - 1:
                    answer_df = pd.concat([answer_df, result_df], axis=1)
                else:
                    answer_df = pd.concat([answer_df, result_df.iloc[:, :-1]], axis=1)
            except Exception as e:
                raise HTTPException(500, str(e))

        answer_df[f'TG{tg_life_num}Life[kWh]'] = answer_df[f'TG{tg_life_num}Life[kWh]'].astype(float)
        answer_df.sort_values(f'TG{tg_life_num}Life[kWh]', axis=0, inplace=True)
        print('time: ', time.time() - start_time)
        return ["step", answer_df]

    @classmethod
    def write_df(cls, write_api, file: File(), batch_size=1000):
        print('write csv', file.filename)

        # check file format
        if not file.content_type == 'text/csv':
            return {"filename": file.filename, "message": "Invalid CSV file", 'status': 'fail',
                    'batch_steps_cnt': ''}
        # check file name
        if len(file.filename.split('-')) < 3:
            return {"filename": file.filename, "message": "Invalid file name", 'status': 'fail'}

        measurement_before = file.filename.split('-')[0]
        measurement = get_measurement_code(measurement_before)
        date_string = file.filename.rsplit('-')[2]
        ymd_string = f"20{date_string[:2]}-{date_string[2:4]}-{date_string[4:]} "

        try:

            # initial_rows = pd.read_csv(file.file, nrows=20)
            # header_row = initial_rows.apply(lambda row: 'Time' in row.values, axis=1).idxmax()+1
            # file.file.seek(0)
            # df = pd.read_csv(file.file, header=header_row)

            df = pd.read_csv(file.file)

            if 'Time' not in df.columns:
                return {'filename': file.filename, 'message': 'csv file has no column', 'status': 'fail'}

            df['TempTime'] = pd.to_datetime(ymd_string + df['Time'], format='%Y-%m-%d %H:%M:%S')
            df['shift'] = (df['Time'] < df['Time'].shift(1)).cumsum()
            df['DateTime'] = df.apply(lambda x: x['TempTime'] + pd.DateOffset(days=x['shift']), axis=1)

            batch_steps_cnt, section_list = save_section_data(measurement,
                                                              df[['DateTime', 'RcpReq[]', 'CoatingLayerN[Layers]']])

            # print('batch_steps_cnt', batch_steps_cnt)
            # print('section_list', section_list)
            if batch_steps_cnt is None and section_list is None:
                return {"filename": file.filename,
                        "message": "File write failed. Batch is still in progress on the first or last row of the file.",
                        'status': 'fail',
                        }

            if len(section_list) == 0:
                df['batch'] = '-'
                df['section'] = '-'
            else:
                for section in section_list:
                    batch_start_time = pd.to_datetime(section.batchStartTime)
                    batch_end_time = pd.to_datetime(section.batchEndTime)

                    df['batch'] = np.where((df['DateTime'] >= batch_start_time) & (df['DateTime'] <= batch_end_time),
                                           section.batchName, '-')
                    df['section'] = '-'

                    for step in range(len(section.steps)):
                        section_start_time = section.steps[step][f'step{step}'][f'step{step}StartTime']
                        section_end_time = section.steps[step][f'step{step}'][f'step{step}EndTime']

                        df.loc[(df['DateTime'] >= section_start_time) & (
                                df['DateTime'] <= section_end_time), 'section'] = f'{step}'

            df.drop(columns=['Time', 'TempTime', 'shift'], inplace=True)

            for column in df.columns:
                if pd.api.types.is_numeric_dtype(df[column]):
                    df[column] = df[column].astype(float)


            tags = ['batch', 'section', 'TG1Life[kWh]', 'TG2Life[kWh]', 'TG4Life[kWh]', 'TG5Life[kWh]']
            # pd.set_option('display.max_rows', None)
            # pd.set_option('display.max_columns', None)
            # print(df.dtypes)
            data = data_frame_to_list_of_points(data_frame=df,
                                                data_frame_measurement_name=measurement,
                                                data_frame_timestamp_column='DateTime',
                                                data_frame_tag_columns=tags,
                                                point_settings=PointSettings())

            write_api.write(bucket=settings.influx_bucket, record=data)
            return {"filename": file.filename, "message": "File successfully written.",
                    'status': 'success',
                    "batch_steps_cnt": batch_steps_cnt}
        except Exception as e:
            logger.error(f"Error fetching item : {e}", exc_info=True)
            return {"filename": file.filename, "message": str(e), 'status': 'fail'}

    @classmethod  # 현재 사용 안함
    async def write_not_df(cls, write_api, file: File(), batch_size=1000):
        global point
        print('write csv', file.filename)

        # check file format
        if not file.content_type == 'text/csv':
            return {"filename": file.filename, "message": "Invalid CSV file"}
        # check file name
        if not cls.checkFileName(file.filename):
            return {"filename": file.filename, "message": "Invalid file name"}

        measurement = file.filename.rsplit('-')[0]
        date_string = file.filename.rsplit('-')[2]
        ymd_string = f"20{date_string[:2]}-{date_string[2:4]}-{date_string[4:]} "

        content = await file.read()
        data = StringIO(content.decode('utf-8'))
        reader = csv.reader(data)

        try:
            cnt = 0
            points = []
            header = [string for string in next(reader) if string != '']  # read first row
            for row in reader:  # read second row ~
                for idx, column in enumerate(header):

                    if idx == 0:
                        point = Point(measurement).time(
                            datetime.strptime(ymd_string + row[idx], '%Y-%m-%d %H:%M:%S')
                            , write_precision=WritePrecision.S)
                    else:
                        value = float(row[idx])
                        point = point.field(column, value)
                        points.append(point)

                if (cnt % batch_size) == 0:
                    write_api.write(settings.influx_bucket, settings.influx_org, points)
                    points.clear()

            # write_api.write(client=self.client, bucket=settings.influx_bucket, org=settings.influx_org,
            #                 record=points)
        except Exception as e:
            return {"filename": file.filename, "message": str(e)}

        return {"filename": file.filename, "message": "Data written"}

    @classmethod
    def createBucket(cls, client: InfluxDBClient):
        bucket_api = client.buckets_api()
        buckets = bucket_api.find_buckets().buckets
        if not any(b.name == settings.influx_bucket for b in buckets):
            bucket_api.create_bucket(bucket_name=settings.influx_bucket, org=settings.influx_org)
