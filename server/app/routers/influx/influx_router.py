import os
from fastapi import APIRouter, File, UploadFile, HTTPException

from influxdb_client import InfluxDBClient

from collections import defaultdict
from typing import List

from starlette.responses import JSONResponse

from app.repository.influx.influx_client import InfluxGTRClient
from app.routers.bokeh.bokeh_router import FacilityData
from app.utils.functions.influx_functions import get_section, get_facilities_info

from config import settings

url = settings.influx_url
token = settings.influx_token
organization = settings.influx_org
bucket = settings.influx_bucket

influx_router = APIRouter(prefix="/facility", tags=['request'])

@influx_router.post("/write")
async def write_influxdb(files: List[UploadFile] = File(...)):
    client = InfluxGTRClient(url=url, token=token, org=organization, bucket_name=bucket)
    return await client.write_csv(files, 1000)

@influx_router.get("/info")
async def get_info_test():
    return get_facilities_info()

@influx_router.post("/read")
async def read_influxdb(conditions: List[FacilityData]):
    return JSONResponse(status_code=200, content={'message': 'success'})