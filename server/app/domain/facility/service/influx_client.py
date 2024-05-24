from datetime import datetime

import pytz
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

from app.domain.correlation.model.correlation_section_data import CorrelationSectionData
from app.domain.facility.model.facility_data import TGLifeData, RequestTGLifeInfo
from app.domain.facility.service.facility_utils import get_measurement_code
from app.domain.facility.service.facility_query import field_by_time_query, execute_query, measurement_list_query, \
    field_list_query, TGLife_time_query, correlation_query, TGLife_count_query, TGLife_cycle_query
from app.domain.section.model.section_data import SectionData
from app.domain.section.service.batch_service import save_section_data

from config import settings

import logging


class InfluxGTRClient:  # GTR: Global Technology Research

    def __init__(self, url: str, token: str, org: str, bucket_name: str) -> None:

        # setting logger
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        self.bucket_name = bucket_name
        self.client = InfluxDBClient(url=url, token=token, org=org, timeout=600000)  # timeout: 2 minute

    async def write_csv(self, files: List[UploadFile] = File(...), batch_size=5000) -> []:
        """
        Write CSV files to InfluxDB

        :param files: facility csv files
        :param batch_size: batch size
        :return: success count, json({"filename": , "message": , 'status': }) list
        """
        # start total time for check time taken
        total_time = time.time()

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

            try:
                df = pd.read_csv(file.file)
                filename = file.filename

                res = self.write_df(df=df, filename=filename, write_api=write_api)
                response.append(res)

                if res['status'] == 'success':
                    success_cnt += 1
            except Exception as e:
                logging.error(e)

            # end time for check time taken
            logging.info(f'file: {file.filename}, time: {time.time() - start_time}')

        write_api.close()
        count = {'count': success_cnt}

        # end total time for check time taken
        logging.info(f'total time: {time.time() - total_time}')

        # resolve seperated batch files - start
        check_list = []  # seperated file list
        idx_list, filename_list = self.checking_write_files(responses=response)  # checking seperated batch files
        for idx in idx_list:
            check_list.append(files[idx])

        logging.info('===========[failed file list]===========')
        logging.info(f'filename list: {filename_list}')
        logging.info(f'idx list: {idx_list}')
        df_list = await self.assemble_csv(check_list)  # assembling seperated files and return dataframe

        for df, filename in zip(df_list, filename_list):  # rewrite reformat df to influxDB
            addition_insert_time = time.time()
            res = self.write_df(df=df, filename=filename, write_api=write_api)
            response.append(res)
            logging.info(f'reformat file: {filename}, time: {time.time() - addition_insert_time}')

            if res['status'] == 'success':
                success_cnt += 2
        # resolve seperated batch files - end

        return count, response

    @classmethod
    def write_df(cls, df: pd.DataFrame, filename: str, write_api: object) -> object:
        """
        Insert Dataframe to InfluxDB

        :param df: dataframe
        :param filename: file name
        :param write_api: client write api
        :return: JSON that success or fail
        """
        measurement = get_measurement_code(filename.split('-')[0])  # measurement : facility name (ex. MASS09)
        date_string = filename.rsplit('-')[2]  # date_string : date string from file (ex. 240101)
        ymd_string = f"20{date_string[:2]}-{date_string[2:4]}-{date_string[4:]} "  # ymd_string : (ex. "2024-01-01 ")

        try:
            # exception for not exist columns
            if 'Time' not in df.columns:
                return {'filename': filename, 'message': 'csv file has no column', 'status': 'fail'}

            # date('2024-01-01 ') + time('12:00:00') and checking the day pass by 'shift' column
            df['TempTime'] = pd.to_datetime(ymd_string + df['Time'], format='%Y-%m-%d %H:%M:%S', utc=True)
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

            return {"filename": filename, "message": "File successfully written.",
                    'status': 'success',
                    "batch_steps_cnt": batch_steps_cnt}
        except Exception as e:
            logging.error(f"Error fetching item : {e}", exc_info=True)
            return {"filename": filename, "message": str(e), 'status': 'fail'}

    def read_facility_info(self):
        """
        Retrieving facility info

        :return: dictionary for facility info
        """
        # facility list (ex. MASS09, MASS10)
        facility_df = execute_query(self.client, measurement_list_query(bucket=self.bucket_name))
        if facility_df is None:
            return None

        facilities = defaultdict(list)
        for facility in facility_df['_value']:
            # field list
            field_df = execute_query(self.client, field_list_query(bucket=self.bucket_name, measurement=facility))

            # answer_fields to list
            fields = [field for field in field_df['_value']]

            # key: facility, value: fields
            facilities[facility] = fields

        return {'result': dict(facilities)}

    def read_parameter_df(self, conditions: List[SectionData], isWindowScale: bool = False) -> []:
        """
        Retrieving dataframe list by parameter & time from influxdb

        :param conditions: query conditions
        :param isWindowScale: option window scale
        :return: dataframe list
        """
        result_df: [pd.DataFrame] = []

        for condition in conditions:

            # query that get data by parameter & time
            query = field_by_time_query(
                bucket=self.bucket_name, facility=condition.facility, field=condition.parameter,
                start_date=condition.startTime, end_date=condition.endTime, isWindowScale=isWindowScale)

            try:
                query_s = time.time()
                df = execute_query(self.client, query)
                logging.info(f"query time: {time.time() - query_s}")

                df['Time'] = pd.to_datetime(df['Time'])
                df.sort_values(by=['Time'], ascending=True, inplace=True)

                if df is None:
                    continue
                df.rename(
                    columns={'_value': f'{condition.facility}-{condition.parameter}'},
                    inplace=True)

                result_df.append(df)
            except Exception as e:
                raise HTTPException(500, str(e))

        return result_df

    def read_TGLife_cycles_info(self, condition: RequestTGLifeInfo):
        df = self.read_TGLife_cycle_info(client=self.client, condition=condition, bucket=self.bucket_name)
        return df

    @classmethod
    def read_TGLife_cycle_info(cls, client, condition: RequestTGLifeInfo, bucket: str):
        try:
            query = TGLife_cycle_query(bucket=bucket, facility=condition.facility, num=condition.tgLifeNum)
            df = execute_query(client=client, query=query)

            df.sort_values(by='Time', ascending=True, inplace=True)
            df.reset_index(drop=True, inplace=True)

            # first row
            first_row = df.iloc[:1]

            # check next tg life cycle start point
            df_startpoint = df[df['Time'].diff() >= pd.Timedelta(days=30)]

            # check tg life cycle end point
            df_endpoint = df_startpoint.copy()
            df_endpoint['Time'] = df_endpoint['Time'] - pd.Timedelta(seconds=1)
            df_endpoint.loc[len(df.index)] = [datetime.now(pytz.utc).replace(microsecond=0)]

            # concat first row, start point, end point
            r_df = pd.concat([first_row, df_startpoint, df_endpoint])

            # sorting
            r_df.sort_values(by='Time', ascending=True, inplace=True)
            r_df.reset_index(drop=True, inplace=True)

            # print('====== result df ======')
            # print(r_df)

            answer = []
            for i in range(0, r_df.shape[0] - 1, 2):
                time_str_i = r_df['Time'].iloc[i].strftime('%Y-%m-%d %H:%M:%S')
                time_str_i1 = r_df['Time'].iloc[i + 1].strftime('%Y-%m-%d %H:%M:%S')

                answer.append({
                    'cycleName': f'cycle-{condition.facility}-{time_str_i}',
                    'startTime': f'{time_str_i[:10]}T{time_str_i[11:]}.000Z',
                    'endTime': f'{time_str_i1[:10]}T{time_str_i1[11:]}.000Z'
                })
            return answer
        except Exception as e:
            raise HTTPException(500, str(e))

        return None

    def read_TGLife_df_list(self, condition: TGLifeData) -> object:
        """
        Retrieving TG data

        :param condition: condition
        :return: dataframe
        """
        df = self.TGLife_df(client=self.client, condition=condition, bucket=self.bucket_name)
        return df

    @classmethod
    def TGLife_df(cls, client, condition, bucket) -> pd.DataFrame:
        """
        Retrieving TGLife dataframe from influxdb

        :param client: influxdb client
        :param condition: tg life condition
        :param bucket: bucket
        :return: dataframe
        """
        try:
            if condition.type == 'time':
                query = TGLife_time_query(bucket=bucket, facility=condition.facility, num=condition.tgLifeNum,
                                          start_date=condition.startTime, end_date=condition.endTime)
            else:
                query = TGLife_count_query(bucket=bucket, facility=condition.facility, num=condition.tgLifeNum,
                                           start_cnt=condition.startCnt, end_cnt=condition.endCnt)

            pd.set_option('display.max_rows', None)  # option that print all row for dataframe
            # pd.set_option('display.max_columns', None)  # option that print all col for dataframe

            result_df = execute_query(client, query)
            result_df.rename(columns={f'TG{condition.tgLifeNum}Life[kWh]_TAG': f'TG{condition.tgLifeNum}Life[kWh]'},
                             inplace=True)

            result_df[f'TG{condition.tgLifeNum}Life[kWh]'] = pd.to_numeric(result_df[
                f'TG{condition.tgLifeNum}Life[kWh]'], errors='coerce')
            result_df['section'] = pd.to_numeric(result_df['section'], errors='coerce')

            result_df.sort_values(by='time', ascending=True, inplace=True)
            result_df.reset_index(drop=True, inplace=True)

            print('========== before df ==========')
            print(result_df)

            del_list = []
            count_list = []
            sum_list = []
            max_list = []
            min_list = []

            del_element = 0
            count_element = 0
            sum_element = 0
            max_element = 0
            min_element = 0
            for i, row in result_df.iterrows():
                if i == result_df.shape[0] - 1:
                    break
                if result_df.loc[i, 'section'] == result_df.loc[i + 1, 'section']:
                    del_element += 1
                    count_element += result_df.loc[i + 1, 'count']
                    sum_element += result_df.loc[i + 1, 'sum']
                    max_element = max(max_element, result_df.loc[i + 1, 'max'])
                    min_element = min(min_element, result_df.loc[i + 1, 'min'])
                else:
                    if count_element != 0:
                        del_list.append([i + 1 - del_element, del_element])
                        count_list.append(count_element)
                        sum_list.append(sum_element)
                        max_list.append(max_element)
                        min_list.append(min_element)

                        del_element = 0
                        count_element = 0
                        sum_element = 0
                        max_element = 0
                        min_element = 0

            if del_element != 0:
                del_list.append([result_df.shape[0] - del_element, del_element])
                count_list.append(count_element)
                sum_list.append(sum_element)
                max_list.append(max_element)
                min_list.append(min_element)

            for delete, count in zip(del_list, count_list):
                del_arr = np.arange(delete[0], delete[0] + delete[1])
                result_df.drop(del_arr, axis=0, inplace=True)
                result_df.loc[delete[0] - 1, 'count'] += count
            result_df.reset_index(drop=True, inplace=True)

            result_df['avg'] = result_df['sum'] / result_df['count']

            print('========== sorted df / add avg column ==========')
            print(result_df)
        except Exception as e:
            raise HTTPException(500, str(e))

        return result_df

    @classmethod
    def checking_write_files(cls, responses: []) -> []:
        """
        Check write file
        Return Seperated files info list

        :param responses: responses
        :return: list, list
        """
        idx_list = []
        filename_list = []
        for idx, response in enumerate(responses):
            if response['message'].startswith('File write failed. '):
                idx_list.append(idx)

        result_idx_list = []
        for i in range(len(idx_list) - 1):
            if idx_list[i] + 1 == idx_list[i + 1]:
                filename_list.append(
                    f"{responses[idx_list[i]]['filename']} and {responses[idx_list[i + 1]]['filename']}")
                result_idx_list.extend([idx_list[i], idx_list[i + 1]])

        return result_idx_list, filename_list

    @classmethod
    async def assemble_csv(cls, files: []) -> List[pd.DataFrame]:
        """
        Assembling seperated csv files

        :param files: files
        :return: dataframe that
        """
        df_list = []
        answer_df = []
        for idx, file in enumerate(files):

            await file.seek(0)  # move file index: 0

            df = pd.read_csv(file.file)
            df_list.append(df)

            if idx % 2 == 1:
                answer_df.append(pd.concat([df_list[idx - 1], df_list[idx]], ignore_index=True))

        return answer_df

    def read_correlation_data(self, condition: CorrelationSectionData):
        print("\n\n\ncondition:", condition)
        # query that get data by parameter & time

        query = correlation_query(
            bucket=self.bucket_name, facility=condition.facility, fields=condition.parameter,
            start_date=condition.startTime,
            end_date=condition.endTime
        )
        try:
            query_s = time.time()
            df = execute_query(self.client, query)
            print('query time ', time.time() - query_s)
            # print("\n\nbefore df:", df)
            # df['Time'] = pd.to_datetime(df['Time'])
            df = df.drop(columns=['Time', '_start', '_stop', '_measurement', 'batch', 'section',
                                  'TG1Life[kWh]_TAG', 'TG2Life[kWh]_TAG', 'TG4Life[kWh]_TAG', 'TG5Life[kWh]_TAG'])
            # print("\n\nafter df:", df)

            if df is None:
                return None
            df.rename(
                columns={'_value': f'{condition.facility}-{condition.parameter}'},
                inplace=True)

        except Exception as e:
            raise HTTPException(500, str(e))
        # pd.set_option('display.max_rows', None)
        # pd.set_option('display.max_columns', None)
        return df

    @classmethod
    def createBucket(cls, client: InfluxDBClient):
        """
        Create Bucket in influxDB if not exist

        :param client: influxdb client
        """
        bucket_api = client.buckets_api()
        buckets = bucket_api.find_buckets().buckets
        if not any(b.name == settings.influx_bucket for b in buckets):
            bucket_api.create_bucket(bucket_name=settings.influx_bucket, org=settings.influx_org)
