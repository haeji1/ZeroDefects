import os
from fastapi import APIRouter, File, UploadFile, HTTPException

from influxdb_client import InfluxDBClient

from collections import defaultdict
from typing import List

from starlette.responses import JSONResponse

from app.models.influx.influx_models import SectionData
from app.repository.influx.influx_client import InfluxGTRClient
from app.routers.bokeh.bokeh_router import FacilityData
from app.utils.functions.influx_functions import get_section, get_facilities_info, get_datas

from config import settings

url = settings.influx_url
token = settings.influx_token
organization = settings.influx_org
bucket = settings.influx_bucket

influx_router = APIRouter(prefix="/facility", tags=['request'])


@influx_router.post("/write")
async def write_influxdb(files: List[UploadFile] = File(...)):
    client = InfluxGTRClient(url=url, token=token, org=organization, bucket_name=bucket)
    content = client.write_csv(files)
    return JSONResponse(status_code=200, content=content)


@influx_router.get("/info")
async def get_info_test():
    return get_facilities_info()


@influx_router.post("/read")
async def read_influxdb():
    sections: List[SectionData] = [SectionData(
        facility="F1494",
        batchName=None,
        parameter="P.PiG201Press[Pa]",
        startTime="2024-02-11T00:29:04.0Z",
        endTime="2024-04-21T01:29:04.0Z"
    ), SectionData(
        facility="F1494",
        batchName=None,
        parameter="P.MF211Ar[sccm]",
        startTime="2024-02-11T00:29:04.0Z",
        endTime="2024-04-21T01:29:04.0Z"
    )]

    client = InfluxGTRClient(url=url, token=token, org=organization, bucket_name=bucket)
    graph_type, graph_df = client.read_data(sections)
    return JSONResponse(status_code=200, content={'result': 'success'})
