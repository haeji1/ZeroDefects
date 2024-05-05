import os
from fastapi import APIRouter, File, UploadFile, HTTPException

from influxdb_client import Point, InfluxDBClient, WritePrecision, WriteOptions

import pandas as pd

from datetime import datetime, timedelta
import time

from collections import defaultdict
from typing import List

from influxdb_client.client.write_api import ASYNCHRONOUS
from starlette.responses import JSONResponse

# from app.repository.influx.influx_client import InfluxGTRClient
from app.routers.bokeh.bokeh_router import FacilityData
from app.utils.functions.influx_functions import get_datas, get_df_TRC, get_section

from config import settings

url = settings.influx_url
token = settings.influx_token
organization = settings.influx_org
bucket = settings.influx_bucket

influx_router = APIRouter(prefix="/facility", tags=['request'])


def create_bucket_if_not_exists(client, bucket_name, org):
    bucket_api = client.buckets_api()
    buckets = bucket_api.find_buckets().buckets
    if not any(b.name == bucket_name for b in buckets):
        bucket_api.create_bucket(bucket_name=bucket_name, org=org)


@influx_router.post("/write")
async def write_influxdb(files: List[UploadFile] = File(...)):
    total_time = 0
    # print('start time: ', start_time)
    batch_size = 5000
    for file in files:
        # start time
        start_time = time.time()

        # csv to data frame
        print(file.filename)
        df = pd.read_csv(file.file)
        df['Previous_Time'] = df['Time'].shift(1)  # 이전 시간을 새 컬럼으로 추가
        measurement = file.filename.split('-')[0]
        date_string = file.filename.split('-')[2]

        # ⭐something implement later
        # exception table name, date info

        # create influxDB client
        client = InfluxDBClient(url=url, token=token, org=organization, timeout=120000)
        write_api = client.write_api(write_options=
                                     WriteOptions(
                                         batch_size=batch_size,
                                         # flush_interval=10000,
                                         # exponential_base=2,
                                         write_type=ASYNCHRONOUS
                                     ))

        # 버킷이 존재하지 않으면 생성
        create_bucket_if_not_exists(client, bucket, organization)

        # index, step
        # 각 로우를 influxDB point로 변환
        points = []
        date_string = f"20{date_string[:2]}-{date_string[2:4]}-{date_string[4:]} "
        cnt = 0
        for _, row in df.iterrows():
            cnt += 1
            # Point 객체를 생성하여 시계열 데이터를 정의합니다.
            # 여기서는 Time 컬럼을 시간으로, 나머지 컬럼들을 필드로 사용합니다.
            time_string = row['Time']  # 시간 형식에 맞춰 조정해야 할 수 있습니다.

            # strptime: 문자열을 시간 객체로
            # strftime: 시간 객체를 문자열로
            if pd.notna(row['Previous_Time']) and row['Time'] < row['Previous_Time']:
                date_time_string = date_string + time_string
                date_time_obj = datetime.strptime(date_time_string, '%Y-%m-%d %H:%M:%S') + timedelta(days=1)
                date_string = date_time_obj.strftime('%Y-%m-%d ')
            else:
                date_time_string = date_string + time_string
                date_time_obj = datetime.strptime(date_time_string, '%Y-%m-%d %H:%M:%S')

            forrmatted_date = date_time_obj.strftime('%Y-%m-%d %H:%M:%S')

            # measurement: ex. F1492
            point = Point(measurement).time(forrmatted_date, write_precision=WritePrecision.S)

            for column in df.columns:
                if column != 'Previous_Time' and column != 'Time' and column[0] != '-':
                    # print('column ', column)
                    try:
                        value = float(row[column])
                        point = point.field(column, value)
                    except ValueError:
                        print(f"Value conversion error for column {column}: {row[column]} : {type(row[column])}")
            points.append(point)

            if (cnt % batch_size) == 0:
                write_api.write(bucket, organization, points)
                points.clear()




        # write_api.write(bucket=bucket, record=points)
        write_api.close()
        client.close()

        # end time
        end_time = time.time()
        total_time += end_time - start_time
        print('time: ', end_time - start_time)
        print('-----------------------')

    print('total time: ', total_time)
    return {'message': 'File uploaded'}

@influx_router.post("/write-test")
async def write_test(files: List[UploadFile] = File(...)):
    client = InfluxGTRClient(url=url, token=token, org=organization, bucket_name=bucket)
    return await client.write_csv(files, 1000)

@influx_router.get("/info")
async def get_info():
    client = InfluxDBClient(url=url, token=token, org=organization)
    query_api = client.query_api()

    get_measurement_query = info_measurements_query(bucket)

    try:
        result = query_api.query(org=organization, query=get_measurement_query)
        measurements = [record.get_value() for record in result[0].records]
        facilities = defaultdict(list)
        for measurement in measurements:
            get_fields_query = info_field_query(bucket, measurement)

            result = query_api.query(org=organization, query=get_fields_query)
            fields = [record.get_value() for record in result[0].records]
            facilities[measurement] = fields

        return {"result": facilities}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@influx_router.post("/read")
async def read_influxdb(conditions: List[FacilityData]):
    # facility_list, parameter_list, df_list = get_datas(conditions)
    # print('--------------------------------')
    # print('get datas: ', get_datas(conditions))
    # print('--------------------------------')
    # print('get df TRC: ', get_df_TRC(conditions[0]))
    print('--------------------------------')
    print('get sections: ', get_section(conditions[0]))

    return JSONResponse(status_code=200, content={'message': 'success'})



def info_measurements_query(b: str) -> str:
    query = f"""
        import "influxdata/influxdb/schema"
        schema.measurements(bucket: "{b}")
        """
    return query
def info_field_query(b: str, measurement: str) -> str:
    query = f"""
        import "influxdata/influxdb/schema"
        schema.fieldKeys(
        bucket: "{b}",
        predicate: (r) => r._measurement == "{measurement}",
        )
        """

    return query