from fastapi import UploadFile, File
from collections import defaultdict
from http.client import HTTPException
import time

import numpy as np
import pandas as pd

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import WriteOptions, ASYNCHRONOUS, PointSettings
from influxdb_client.client.write.dataframe_serializer import data_frame_to_list_of_points

from typing import List
from loguru import logger

from app.domain.facility.model.facility_data import TGLifeData
from app.domain.facility.service.facility_utils import get_measurement_code
from app.domain.facility.service.facility_query import field_by_time_query, execute_query, info_measurements_query, \
    info_field_query, TGLife_query
from app.domain.section.model.section_data import SectionData
from app.domain.section.service.batch_service import save_section_data

from config import settings

# from influxapi.schemas import InfluxWaveRecord

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InfluxGTRClient:  # GTR: Global Technology Research

    # constructor
    def __init__(self, url: str, token: str, org: str, bucket_name: str) -> None:
        self.bucket_name = bucket_name
        self.client = InfluxDBClient(url=url, token=token, org=org, timeout=120000)  # timeout: 2 minute

    # write
    async def write_csv(self, files: List[UploadFile] = File(...), batch_size=5000) -> []:
        total_time = time.time()  # start total time for check time taken

        # create write api
        write_api = self.client.write_api(write_options=WriteOptions(
            batch_size=batch_size,
            write_type=ASYNCHRONOUS
        ))

        # create bucket if not exist
        self.createBucket(self.client)

        response = []  # result list for csv file input
        success_cnt = 0  # success count
        for file in files:

            # start time for check time taken
            start_time = time.time()

            res = await self.write_df(write_api, file)
            if res['status'] == 'success':
                success_cnt += 1
            response.append(res)

            # end time for check time taken
            print('time: ', time.time() - start_time)
            print('-----------------------')

        write_api.close()
        count = {'count': success_cnt}

        # end total time for check time taken
        print('total time: ', time.time() - total_time)

        # resolve seperated batch files - start
        check_list = [] # seperated file list
        idx_list, filename_list = self.checking_writed_files(responses=response)    # checking seperated batch files
        for idx in idx_list:
            check_list.append(files[idx])
        print('===========[idx, filename]===========')
        print(idx_list)
        print(filename_list)
        df_list = await self.assemble_csv(check_list)   # assembling seperated files and return dataframe

        for df, filename in zip(df_list, filename_list):    # rewrite df to influxDB
            response.append(self.write_by_df(df=df, filename=filename, write_api=write_api))
        # resolve seperated batch files - end

        return count, response

    @classmethod
    async def write_df(cls, write_api, file: File()):
        # write csv file to influxDB

        # check file format
        if not file.content_type == 'text/csv':
            return {"filename": file.filename, "message": "Invalid CSV file", 'status': 'fail',
                    'batch_steps_cnt': ''}

        # check file name
        if len(file.filename.split('-')) < 3:
            return {"filename": file.filename, "message": "Invalid file name", 'status': 'fail'}

        measurement = get_measurement_code(file.filename.split('-')[0])  # measurement : facility name (ex. MASS09)
        date_string = file.filename.rsplit('-')[2]  # date_string : date string from file (ex. 240101)
        ymd_string = f"20{date_string[:2]}-{date_string[2:4]}-{date_string[4:]} "  # ymd_string : (ex. "2024-01-01 ")

        try:
            df = pd.read_csv(file.file)

            # exception for not exist columns
            if 'Time' not in df.columns:
                return {'filename': file.filename, 'message': 'csv file has no column', 'status': 'fail'}

            # date('2024-01-01 ') + time('12:00:00') and checking the day pass by 'shift' column
            # UTC+0
            df['TempTime'] = pd.to_datetime(ymd_string + df['Time'], format='%Y-%m-%d %H:%M:%S', utc=True)
            df['shift'] = (df['Time'] < df['Time'].shift(1)).cumsum()
            # UTC+0
            df['DateTime'] = df.apply(lambda x: x['TempTime'] + pd.Timedelta(days=int(x['shift'])), axis=1)

            # save batch, step to mongo
            batch_steps_cnt, section_list = save_section_data(measurement,
                                                              df[['DateTime', 'RcpReq[]', 'CoatingLayerN[Layers]']])

            # 파일의 첫번 째 행 혹은 마지막 행에 배치나 스탭이 존재하는 경우 해당 배치나 스탭을 하나의 온전한 사이클로 볼 수 없어서 예외 처리
            if batch_steps_cnt is None and section_list is None:
                return {"filename": file.filename,
                        "message": "File write failed. Batch is still in progress on the first or last row of the file.",
                        'status': 'fail',
                        }

            if len(section_list) == 0:  # no batch in file
                df['batch'] = '-'
                df['section'] = '-'
            else:  # exist batch in file
                for section in section_list:  # write value to 'batch' column
                    batch_start_time = pd.to_datetime(section.batchStartTime, utc=True)
                    batch_end_time = pd.to_datetime(section.batchEndTime, utc=True)

                    # if (batch_start_time < 'DateTime' < batch_end_time) 'batch' is section.batchName else '-'
                    df['batch'] = np.where((df['DateTime'] >= batch_start_time) & (df['DateTime'] <= batch_end_time),
                                           section.batchName, '-')
                    df['section'] = '-'
                    for step in range(len(section.steps)):  # write value to 'section' column
                        section_start_time = section.steps[step][f'step{step}'][f'step{step}StartTime']
                        section_end_time = section.steps[step][f'step{step}'][f'step{step}EndTime']

                        # if (section_start_time < 'DateTime' < section_end_time) 'batch' is step number
                        df.loc[(df['DateTime'] >= section_start_time) & (
                                df['DateTime'] <= section_end_time), 'section'] = f'{step}'

            # drop not using columns
            df.drop(columns=['Time', 'TempTime', 'shift'], inplace=True)

            # if dtype is number, dtype to float
            for column in df.columns:
                if pd.api.types.is_numeric_dtype(df[column]):
                    df[column] = df[column].astype(float)

            # copy tag columns
            df = pd.concat([df, df[['TG1Life[kWh]', 'TG2Life[kWh]', 'TG4Life[kWh]', 'TG5Life[kWh]']]
                           .rename(columns=lambda x: x + '_TAG')], axis=1)

            # setting tags
            tags = ['batch', 'section', 'TG1Life[kWh]_TAG', 'TG2Life[kWh]_TAG', 'TG4Life[kWh]_TAG', 'TG5Life[kWh]_TAG']

            # data for write
            data = data_frame_to_list_of_points(data_frame=df,  # data
                                                data_frame_measurement_name=measurement,  # measurement(ex. MASS09)
                                                data_frame_timestamp_column='DateTime',  # timestamp
                                                data_frame_tag_columns=tags,  # tags
                                                point_settings=PointSettings())  # default settings

            write_api.write(bucket=settings.influx_bucket, record=data)

            return {"filename": file.filename, "message": "File successfully written.",
                    'status': 'success',
                    "batch_steps_cnt": batch_steps_cnt}

        except Exception as e:
            logger.error(f"Error fetching item : {e}", exc_info=True)
            return {"filename": file.filename, "message": str(e), 'status': 'fail'}

    @classmethod
    def write_by_df(cls, df: pd.DataFrame, filename: str, write_api):

        measurement = get_measurement_code(filename.split('-')[0])  # measurement : facility name (ex. MASS09)
        date_string = filename.rsplit('-')[2]  # date_string : date string from file (ex. 240101)
        ymd_string = f"20{date_string[:2]}-{date_string[2:4]}-{date_string[4:]} "  # ymd_string : (ex. "2024-01-01 ")

        try:
            # exception for not exist columns
            if 'Time' not in df.columns:
                return {'filename': filename, 'message': 'csv file has no column', 'status': 'fail'}

            # date('2024-01-01 ') + time('12:00:00') and checking the day pass by 'shift' column
            df['TempTime'] = pd.to_datetime(ymd_string + df['Time'], format='%Y-%m-%d %H:%M:%S')
            df['shift'] = (df['Time'] < df['Time'].shift(1)).cumsum()
            df['DateTime'] = df.apply(lambda x: x['TempTime'] + pd.DateOffset(days=x['shift']), axis=1)

            # save batch, step to mongo
            batch_steps_cnt, section_list = save_section_data(measurement,
                                                              df[['DateTime', 'RcpReq[]', 'CoatingLayerN[Layers]']])

            # 파일의 첫번 째 행 혹은 마지막 행에 배치나 스탭이 존재하는 경우 해당 배치나 스탭을 하나의 온전한 사이클로 볼 수 없어서 예외 처리
            if batch_steps_cnt is None and section_list is None:
                return {"filename": filename,
                        "message": "File write failed. Batch is still in progress on the first or last row of the file.",
                        'status': 'fail',
                        }

            if len(section_list) == 0:  # no batch in file
                df['batch'] = '-'
                df['section'] = '-'
            else:  # exist batch in file
                for section in section_list:  # write value to 'batch' column
                    batch_start_time = pd.to_datetime(section.batchStartTime)
                    batch_end_time = pd.to_datetime(section.batchEndTime)

                    # if (batch_start_time < 'DateTime' < batch_end_time) 'batch' is section.batchName else '-'
                    df['batch'] = np.where((df['DateTime'] >= batch_start_time) & (df['DateTime'] <= batch_end_time),
                                           section.batchName, '-')
                    df['section'] = '-'
                    for step in range(len(section.steps)):  # write value to 'section' column
                        section_start_time = section.steps[step][f'step{step}'][f'step{step}StartTime']
                        section_end_time = section.steps[step][f'step{step}'][f'step{step}EndTime']

                        # if (section_start_time < 'DateTime' < section_end_time) 'batch' is step number
                        df.loc[(df['DateTime'] >= section_start_time) & (
                                df['DateTime'] <= section_end_time), 'section'] = f'{step}'

            # drop not using columns
            df.drop(columns=['Time', 'TempTime', 'shift'], inplace=True)

            # if dtype is number, dtype to float
            for column in df.columns:
                if pd.api.types.is_numeric_dtype(df[column]):
                    df[column] = df[column].astype(float)

            # copy tag columns
            df = pd.concat([df, df[['TG1Life[kWh]', 'TG2Life[kWh]', 'TG4Life[kWh]', 'TG5Life[kWh]']]
                           .rename(columns=lambda x: x + '_TAG')], axis=1)

            # setting tags
            tags = ['batch', 'section', 'TG1Life[kWh]_TAG', 'TG2Life[kWh]_TAG', 'TG4Life[kWh]_TAG', 'TG5Life[kWh]_TAG']

            # data for write
            data = data_frame_to_list_of_points(data_frame=df,  # data
                                                data_frame_measurement_name=measurement,  # measurement(ex. MASS09)
                                                data_frame_timestamp_column='DateTime',  # timestamp
                                                data_frame_tag_columns=tags,  # tags
                                                point_settings=PointSettings())  # default settings

            write_api.write(bucket=settings.influx_bucket, record=data)

            return {"filename": filename, "message": "DataFrame that assembled seperated files successfully written.",
                    'status': 'success',
                    "batch_steps_cnt": batch_steps_cnt}
        except Exception as e:
            logger.error(f"Error fetching item : {e}", exc_info=True)
            return {"filename": filename, "message": str(e), 'status': 'fail'}

    # facility info
    def read_info(self):
        # facility list (ex. MASS09, MASS 10)
        answer_measurements = execute_query(self.client, info_measurements_query(b=self.bucket_name))

        facilities = defaultdict(list)
        for measurement in answer_measurements['_value']:
            # column list (ex. volt, press ...)
            answer_fields = self.client.query_api().query_data_frame(
                info_field_query(b=self.bucket_name, measurement=measurement))

            # answer_fields to list
            fields = [field for field in answer_fields['_value']]

            # key: measurement, value: fields
            facilities[measurement] = fields

        return {'result': dict(facilities)}

    # get data by parameter & time from influxdb
    def read_data(self, conditions: List[SectionData]) -> []:
        result_df: [pd.DataFrame] = []

        for condition in conditions:
            print("\n\n\ncondition:", condition)
            # query that get data by parameter & time
            query = field_by_time_query(
                b=self.bucket_name, facility=condition.facility, field=condition.parameter,
                start_date=condition.startTime, end_date=condition.endTime)
            try:
                query_s = time.time()
                df = execute_query(self.client, query)
                print('query time ', time.time() - query_s)
                print("\n\nbefore df:", df)
                df['Time'] = pd.to_datetime(df['Time'])
                print("\n\nafter df:", df)

                if df is None:
                    continue
                df.rename(
                    columns={'_value': f'{condition.facility}-{condition.parameter}'},
                    inplace=True)

                result_df.append(df)
            except Exception as e:
                raise HTTPException(500, str(e))
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        # print(result_df)
        return result_df

    def read_TG_data(self, condition: TGLifeData) -> object:

        start_time = time.time()

        # exception not exist facility
        if condition.facility not in self.read_info()['result'].keys():
            return None

        # exception not exist tg_life number
        if condition.tg_life_num not in ['1', '2', '4', '5']:
            return None

        if condition.statistics_list is None or len(condition.statistics_list) == 0:
            statistics_list = ["AVG"]
        else:
            statistics_list = condition.statistics_list

        # exception statistics elements
        statistics_list = [statistics for statistics in statistics_list
                           if statistics in ["AVG", "MAX", "MIN", "STDDEV"]]

        answer_df = pd.DataFrame()
        for idx, statistics in enumerate(statistics_list):

            # count_flag : flag for get tg_life count column, for performance improve
            count_flag = False
            if idx == 0:
                count_flag = True

            # get tg_life
            query = TGLife_query(b=self.bucket_name, facility=condition.facility, tg_life_num=condition.tg_life_num,
                                 start_date=condition.startTime, end_date=condition.endTime, type=statistics,
                                 count=count_flag)
            try:
                result_df = execute_query(self.client, query)

                # rename (ex. P.TG1I[A] -> AVG-P.TG1I[A])
                result_df.rename(
                    columns={f'P.TG{condition.tg_life_num}I[A]': f'{statistics}-P.TG{condition.tg_life_num}I[A]',
                             f'P.TG{condition.tg_life_num}Pwr[kW]': f'{statistics}-P.TG{condition.tg_life_num}Pwr[kW]',
                             f'P.TG{condition.tg_life_num}V[V]': f'{statistics}-P.TG{condition.tg_life_num}V[V]',
                             f'TG{condition.tg_life_num}Life[kWh]_TAG': f'TG{condition.tg_life_num}Life[kWh]'},
                    inplace=True)

                # case classification, for performance improve
                if idx == 0:
                    answer_df = pd.concat([answer_df, result_df[[
                        f'TG{condition.tg_life_num}Life[kWh]',
                        'count',
                        f'{statistics}-P.TG{condition.tg_life_num}I[A]',
                        f'{statistics}-P.TG{condition.tg_life_num}Pwr[kW]',
                        f'{statistics}-P.TG{condition.tg_life_num}V[V]',
                    ]]], axis=1)
                else:
                    answer_df = pd.concat([answer_df, result_df[[
                        f'{statistics}-P.TG{condition.tg_life_num}I[A]',
                        f'{statistics}-P.TG{condition.tg_life_num}Pwr[kW]',
                        f'{statistics}-P.TG{condition.tg_life_num}V[V]',
                    ]]], axis=1)
            except Exception as e:
                raise HTTPException(500, str(e))

        # sorting by TGLife[kWh]
        answer_df[f'TG{condition.tg_life_num}Life[kWh]'] \
            = answer_df[f'TG{condition.tg_life_num}Life[kWh]'].astype(float)
        answer_df.sort_values(f'TG{condition.tg_life_num}Life[kWh]', axis=0, inplace=True)
        print('time: ', time.time() - start_time)
        return answer_df

    @classmethod
    def checking_writed_files(cls, responses: []) -> []:

        seperated_flag = 0
        idx_list = []
        filename_list = []
        for idx, response in enumerate(responses):
            if response['message'].startswith('File write failed. '):
                idx_list.append(idx)
            # if seperated_flag == 2:
            #     if idx-1 in idx_list:
            #         seperated_flag = 0
            #         filename_list.append(responses[idx-1]['filename'])
            #     else:
            #         seperated_flag = 1
            #         idx_list = idx_list.pop(-1)

        result_idx_list = []
        for i in range(len(idx_list) - 1):
            if idx_list[i] + 1 == idx_list[i + 1]:
                filename_list.append(responses[idx_list[i]]['filename'])
                result_idx_list.extend([idx_list[i], idx_list[i + 1]])

        return result_idx_list, filename_list

    @classmethod
    async def assemble_csv(cls, files: []) -> List[pd.DataFrame]:
        df_list = []
        answer_df = []
        for idx, file in enumerate(files):
            await file.seek(0)
            df = pd.read_csv(file.file)
            df_list.append(df)

            if idx % 2 == 1:
                answer_df.append(pd.concat([df_list[idx-1], df_list[idx]], ignore_index=True))

        return answer_df

    @classmethod
    def createBucket(cls, client: InfluxDBClient):
        bucket_api = client.buckets_api()
        buckets = bucket_api.find_buckets().buckets
        if not any(b.name == settings.influx_bucket for b in buckets):
            bucket_api.create_bucket(bucket_name=settings.influx_bucket, org=settings.influx_org)
