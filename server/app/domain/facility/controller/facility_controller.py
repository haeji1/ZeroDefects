import os
from fastapi import APIRouter, File, UploadFile, HTTPException


from typing import List

from starlette.responses import JSONResponse

from config import settings
from domain.facility.model.facility_data import FacilityData
from domain.facility.repository.facility_repository import FacilityRepository
from domain.facility.service.facility_function import get_facilities_info

url = settings.influx_url
token = settings.influx_token
organization = settings.influx_org
bucket = settings.influx_bucket

facility_router = APIRouter(prefix="/facility", tags=['request'])


@facility_router.post("/write")
async def write_influxdb(files: List[UploadFile] = File(...)):
    client = FacilityRepository(url=url, token=token, org=organization, bucket_name=bucket)
    return await client.write_csv(files, 1000)


@facility_router.get("/info")
async def get_info_test():
    return get_facilities_info()


@facility_router.post("/read")
async def read_influxdb(conditions: List[FacilityData]):
    return JSONResponse(status_code=200, content={'message': 'success'})
