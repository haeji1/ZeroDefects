import os
from fastapi import APIRouter, File, UploadFile, HTTPException

from influxdb_client import InfluxDBClient

from collections import defaultdict
from typing import List

from starlette.responses import JSONResponse

from app.repository.influx.influx_client import InfluxGTRClient
from app.routers.bokeh.bokeh_router import FacilityData
from app.utils.functions.influx_functions import get_section

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
    client = InfluxGTRClient(url=url, token=token, org=organization, bucket_name=bucket)

    # How to use? - for gold money
    # /app.repository.influx.influx_client.py -> method name: write_df (105 line)

    return await client.write_csv(files, 1000)

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
