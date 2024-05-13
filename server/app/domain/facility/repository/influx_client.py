import csv
from collections import defaultdict
from datetime import datetime, timedelta
import time
from http.client import HTTPException
from io import StringIO

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
from app.domain.facility.service.facility_query import field_time_query, execute_query, info_measurements_query, \
    info_field_query
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
        for file in files:
            # start time
            start_time = time.time()

            # await self.write_not_df(write_api, file, batch_size)
            response.append(self.write_df(write_api, file, batch_size))

            # end time
            print('time: ', time.time() - start_time)
            print('-----------------------')

        write_api.close()
        print('total time: ', time.time() - total_time)
        return response
    def read_data(self, conditions: List[SectionData]) -> []:
        start_time = time.time()
        result_df = pd.DataFrame()

        # conditions length == 1
        if len(conditions) == 1:
            query = field_time_query(
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
                query = field_time_query(
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
            answer_fields = self.client.query_api().query_data_frame(info_field_query(b=self.bucket_name, measurement=measurement))

            fields = [field for field in answer_fields['_value']]
            facilities[measurement] = fields

        return {'result': dict(facilities)}

    @classmethod
    def write_df(cls, write_api, file: File(), batch_size=1000):
        print('write csv', file.filename)

        # check file format
        if not file.content_type == 'text/csv':
            return {"filename": file.filename, "message": "Invalid CSV file"}
        # check file name
        if len(file.filename.split('-')) < 3:
            return {"filename": file.filename, "message": "Invalid file name"}

        measurement_before = file.filename.split('-')[0]
        measurement = get_measurement_code(measurement_before)
        date_string = file.filename.rsplit('-')[2]
        ymd_string = f"20{date_string[:2]}-{date_string[2:4]}-{date_string[4:]} "

        try:
            df = pd.read_csv(file.file)

            df['TempTime'] = pd.to_datetime(ymd_string + df['Time'], format='%Y-%m-%d %H:%M:%S')
            df['shift'] = (df['Time'] < df['Time'].shift(1)).cumsum()
            df['DateTime'] = df.apply(lambda x: x['TempTime'] + pd.DateOffset(days=x['shift']), axis=1)

            batch_steps_cnt = save_section_data(measurement, df[['DateTime', 'RcpReq[]', 'CoatingLayerN[Layers]']])
            # print("write_df:", df[['DateTime', 'RcpReq[]', 'CoatingLayerN[Layers]']])

            df_modified = df.drop(columns=['Time', 'TempTime', 'shift'])
            float_cols = df_modified.columns.drop('DateTime')
            df_modified[float_cols] = df_modified[float_cols].astype(float)

            data = data_frame_to_list_of_points(data_frame=df_modified,
                                                data_frame_measurement_name=measurement,
                                                data_frame_timestamp_column='DateTime',
                                                point_settings=PointSettings())

            write_api.write(bucket=settings.influx_bucket, record=data)
            return {"filename": file.filename, "message": "file successfully written.", "batch_steps_cnt": batch_steps_cnt}
        except Exception as e:
            logger.error(f"Error fetching item : {e}", exc_info=True)
            return {"filename": file.filename, "message": str(e)}

    # @classmethod  # 현재 사용 안함
    # def write_df(cls, write_api, file: File(), batch_size=1000):
    #     print('write csv', file.filename)
    #
    #     # check file format
    #     if not file.content_type == 'text/csv':
    #         return {"filename": file.filename, "message": "Invalid CSV file"}
    #     # check file name
    #     if len(file.filename.split('-')) < 3:
    #         return {"filename": file.filename, "message": "Invalid file name"}
    #
    #     measurement = file.filename.rsplit('-')[0]
    #     date_string = file.filename.rsplit('-')[2]
    #     ymd_string = f"20{date_string[:2]}-{date_string[2:4]}-{date_string[4:]} "
    #
    #     try:
    #         df = pd.read_csv(file.file)
    #
    #         df['TempTime'] = pd.to_datetime(ymd_string + df['Time'])
    #         df['shift'] = (df['Time'] < df['Time'].shift(1)).cumsum()
    #         df['DateTime'] = df.apply(lambda x: x['TempTime'] + pd.DateOffset(days=x['shift']), axis=1)
    #
    #         save_section_data(measurement, df[['DateTime', 'RcpReq[]', 'CoatingLayerN[Layers]']])
    #         # print(df[['DateTime', 'RcpReq[]', 'CoatingLayerN[Layers]']])
    #
    #         df_modified = df.drop(columns=['Time', 'TempTime', 'shift'])
    #         float_cols = df_modified.columns.drop('DateTime')
    #         df_modified[float_cols] = df_modified[float_cols].astype(float)
    #
    #         data = data_frame_to_list_of_points(data_frame=df_modified,
    #                                             data_frame_measurement_name=measurement,
    #                                             data_frame_timestamp_column='DateTime',
    #                                             point_settings=PointSettings())
    #
    #         write_api.write(bucket=settings.influx_bucket, record=data)
    #         return {"filename": file.filename, "message": "file successfully written"}
    #     except Exception as e:
    #         logger.error(f"Error fetching item : {e}", exc_info=True)
    #         return {"filename": file.filename, "message": str(e)}

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
