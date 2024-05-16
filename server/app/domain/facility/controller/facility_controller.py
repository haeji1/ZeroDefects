from fastapi import APIRouter, File, UploadFile
from starlette.responses import JSONResponse

from typing import List

from app.domain.facility.model.facility_data import TGLifeData
from app.domain.facility.repository.influx_client import InfluxGTRClient
from app.domain.facility.service.facility_function import get_facilities_info, get_TG_datas

from config import settings

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


# for test
@facility_router.get("/info")
async def get_info_test():
    return get_facilities_info()


# for test
@facility_router.post("/read/tg")
async def read_tg_influxdb(model: TGLifeData):
    try:
        contents = get_TG_datas(model)
        if contents is None:
            return JSONResponse(status_code=400, content={'msg': 'not exist data'})
        else:
            print(contents)
            return JSONResponse(status_code=200, content={'msg': 'success'})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content={'msg': str(e)})
