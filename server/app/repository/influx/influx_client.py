import csv
from datetime import datetime, timedelta
import time
from io import StringIO

import pandas as pd
from fastapi import UploadFile, File
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS, WriteOptions, ASYNCHRONOUS
from influxdb_client.client.write.dataframe_serializer import data_frame_to_list_of_points

from typing import List, Any
from loguru import logger
from starlette.responses import JSONResponse
from urllib3.exceptions import NewConnectionError
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
        self.client = InfluxDBClient(url=url, token=token, org=org)

    # write
    async def write_csv(self, files: List[UploadFile] = File(...), batch_size=900) -> JSONResponse:
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
        return JSONResponse(status_code=200, content=response)

    @classmethod
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
    def write_df(cls, write_api, file: File(), batch_size=1000):
        print('write csv', file.filename)
        start_time = time.time()

        # check file format
        if not file.content_type == 'text/csv':
            return {"filename": file.filename, "message": "Invalid CSV file"}
        # check file name
        if not cls.checkFileName(file.filename):
            return {"filename": file.filename, "message": "Invalid file name"}

        measurement = file.filename.rsplit('-')[0]
        date_string = file.filename.rsplit('-')[2]
        ymd_string = f"20{date_string[:2]}-{date_string[2:4]}-{date_string[4:]} "

        try:
            df = pd.read_csv(file.file)
            # df['Previous_Time'] = df['Time'].shift(1)  # 이전 시간을 새 컬럼으로 추가
            # df['Date_Time'] = df['Time']

            # points = []
            # cnt = 0

            df['DateTime'] = pd.to_datetime(ymd_string + df['Time'])
            df['Day_Shift'] = (df['Time'] < df['Time'].shift(1)).cumsum()
            df['Adjusted_DateTime'] = df.apply(lambda x: x['DateTime'] + pd.DateOffset(days=x['Day_Shift']), axis=1)

            point_settings = {
                "data_frame_measurement_name": measurement,
                "data_frame_tag_columns": [],
                "data_frame_timestamp_column": "Adjusted_DateTime",
                "data_frame_timestamp_timezone": "UTC",
                "defaultTags": {'samsam'}
            }

            df_modified = df.drop(columns=['DateTime', 'Time', 'Day_Shift'])
            data = data_frame_to_list_of_points(data_frame=df_modified,
                                                point_settings=point_settings,
                                                data_frame_measurement_name=measurement,
                                                data_frame_tag_columns=[],
                                                defaultTags={'samsam'},
                                                data_frame_timestamp_column='Adjusted_DateTime',
                                                data_frame_timestamp_timezone="UTC",
                                                precision=WritePrecision.S)
            write_api.write(data, point_settings=point_settings, bucket=settings.influx_bucket, org=settings.influx_org)

            # for _, row in df.iterrows():
            #     cnt += 1
            #
            #     if pd.notna(row['Previous_Time']) and row['Time'] < row['Previous_Time']:
            #         date_obj = datetime.strptime(ymd_string + row['Time'], '%Y-%m-%d %H:%M:%S') + timedelta(days=1)
            #         row['Date_Time'] = datetime.strftime(date_obj, '%Y-%m-%d %H:%M:%S')
            #     else:
            #         date_obj = datetime.strptime(ymd_string + row['Time'], '%Y-%m-%d %H:%M:%S')
            #         row['Date_Time'] = datetime.strftime(date_obj, '%Y-%m-%d %H:%M:%S')


                # point = Point(measurement).time(
                #             datetime.strftime(date_obj, '%Y-%m-%d %H:%M:%S')
                #             , write_precision=WritePrecision.S)

                # InfluxDB에 데이터를 씁니다.
                # write_api.write(data, bucket=settings.influx_bucket, org=settings.influx_org)
                # for column in df.columns:
                #     if column != 'Previous_Time' and column != 'Time':
                #         try:
                #             value = float(row[column])
                #             point = point.field(column, value)
                #         except ValueError:
                #             print(f"Value conversion error for column {column}: {row[column]} : {type(row[column])}")

                # points.append(point)

                # if (cnt % batch_size) == 0:
                #     write_api.write(settings.influx_bucket, settings.influx_org, points)
                #     points.clear()

            # write_api.write(data, point_settings=point_settings, bucket=settings.influx_bucket, org=settings.influx_org)

        except Exception as e:
            logger.error(f"Error fetching item : {e}", exc_info=True)
            return {"filename": file.filename, "message": str(e)}

        # end time
        print('time: ', time.time() - start_time)
        print('-----------------------')

        return {"filename": file.filename, "message": "Data written"}

    @classmethod
    def checkFileName(cls, filename: str) -> bool:
        if len(filename.split('-')) > 2:
            return True

    @classmethod
    def createBucket(cls, client: InfluxDBClient):
        bucket_api = client.buckets_api()
        buckets = bucket_api.find_buckets().buckets
        if not any(b.name == settings.influx_bucket for b in buckets):
            bucket_api.create_bucket(bucket_name=settings.influx_bucket, org=settings.influx_org)