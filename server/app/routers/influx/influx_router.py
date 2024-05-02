import os
from fastapi import APIRouter, File, UploadFile, HTTPException, Query, Body

from influxdb_client import Point, InfluxDBClient, WritePrecision, WriteOptions

import pandas as pd

from datetime import datetime, timedelta

from collections import defaultdict
from typing import List, Dict, Any

from dotenv import load_dotenv
from pydantic import BaseModel

from app.routers.bokehgraph.bokeh_router import FacilityData
from app.routers.influx.influx_utils import influx_list_query

load_dotenv()

url = os.getenv('INFLUXDB_URL')
token = os.getenv('INFLUXDB_TOKEN')
organization = os.getenv('INFLUXDB_ORG')
bucket = os.getenv('INFLUXDB_BUCKET')

influx_router = APIRouter(prefix="/facility", tags=['influx'])

def create_bucket_if_not_exists(client, bucket_name, org):
    bucket_api = client.buckets_api()
    buckets = bucket_api.find_buckets().buckets
    if not any(b.name == bucket_name for b in buckets):
        bucket_api.create_bucket(bucket_name=bucket_name, org=org)
@influx_router.post("/write")
async def write_influxdb(files: List[UploadFile] = File(...)):
    print('token', os.getenv('INFLUXDB_TOKEN'))
    for file in files:
        # csv to data frame
        df = pd.read_csv(file.file)
        df['Previous_Time'] = df['Time'].shift(1)  # 이전 시간을 새 컬럼으로 추가
        measurement = file.filename.split('-')[0]
        date_string = file.filename.split('-')[2]

        # ⭐something implement later
        # exception table name, date info

        # create influxDB client
        client = InfluxDBClient(url=url, token=token, org=organization)
        write_api = client.write_api(write_options=WriteOptions(batch_size=10))

        # 버킷이 존재하지 않으면 생성
        create_bucket_if_not_exists(client, bucket, organization)

        # index, step
        # 각 로우를 influxDB point로 변환
        points = []
        date_string = f"20{date_string[:2]}-{date_string[2:4]}-{date_string[4:]} "
        for _, row in df.iterrows():
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
                    print('column ', column)
                    point = point.field(column, row[column])
            points.append(point)

        write_api.write(bucket=bucket, record=points)
        write_api.close()
        client.close()

    return {'message': 'File uploaded'}

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

    facility_list, prameter_list, df_list = influx_list_query(conditions)

    print('facility_list', facility_list)
    print('prameter_list', prameter_list)
    print('df_list', df_list)
    # facility_list, parameter_list, df_list를 활용해서 bokeh 그리고 return 하면돼

    return {'result': facility_list}