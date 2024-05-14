import os
from fastapi import APIRouter, File, UploadFile, HTTPException

from collections import defaultdict
from typing import List

from app.domain.facility.model.facility_data import TGLifeData
from app.domain.facility.repository.influx_client import InfluxGTRClient
from config import settings
from starlette.responses import JSONResponse

from app.domain.facility.service.facility_function import get_facilities_info

url = settings.influx_url
token = settings.influx_token
organization = settings.influx_org
bucket = settings.influx_bucket

facility_router = APIRouter(prefix="/facility", tags=['request'])


@facility_router.post("/write")
async def write_influxdb(files: List[UploadFile] = File(...)):
    client = InfluxGTRClient(url=url, token=token, org=organization, bucket_name=bucket)
    contents = client.write_csv(files)
    for content in contents:
        print("content:", content)
    return JSONResponse(status_code=200, content=contents)


@facility_router.get("/info")
async def get_info_test():
    return get_facilities_info()


@facility_router.post("/read")
async def read_influxdb():
    return

@facility_router.post("/read/tg")
async def read_tg_influxdb(model: TGLifeData):
    client = InfluxGTRClient(url=url, token=token, org=organization, bucket_name=bucket)
    try:
        client.read_TG_data(facility=model.facility, tg_life_num=model.tg_life,
                                  start_date=model.startTime, end_date=model.endTime)
    except Exception as e:
        return JSONResponse(status_code=400, content={'msg': str(e)})

    return JSONResponse(status_code=200, content={'msg': 'success'})
