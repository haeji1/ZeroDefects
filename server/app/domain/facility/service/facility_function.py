from fastapi import UploadFile, File
from http.client import HTTPException
from typing import List

import warnings

from influxdb_client.client.warnings import MissingPivotFunction
from influxdb_client import InfluxDBClient

from app.domain.correlation.model.correlation_section_data import CorrelationSectionData
from app.domain.facility.model.facility_data import FacilityData, TGLifeData
from app.domain.facility.repository.influx_client import InfluxGTRClient
from app.domain.facility.service.facility_query import section_query, execute_query
from app.domain.section.model.section_data import SectionData

from config import settings

url = settings.influx_url
token = settings.influx_token
organization = settings.influx_org
bucket = settings.influx_bucket

warnings.simplefilter('ignore', MissingPivotFunction)


# --------- functions --------- #

async def write_files(files: List[UploadFile] = File(...)):
    client = InfluxGTRClient(url=url, token=token, org=organization, bucket_name=bucket)
    contents = await client.write_csv(files)
    return contents


def get_facilities_info():
    client = InfluxGTRClient(url=url, token=token, org=organization, bucket_name=bucket)
    contents = client.read_info()
    return contents


# get data
def get_datas(conditions: List[SectionData], all: bool = False):
    client = InfluxGTRClient(url=url, token=token, org=organization, bucket_name=bucket)
    contents = client.read_data(conditions, all=all)
    return contents


def get_TG_datas(condition: TGLifeData):
    client = InfluxGTRClient(url=url, token=token, org=organization, bucket_name=bucket)
    contents = client.read_TG_data(condition)
    return contents


def get_correlation_datas(condition: CorrelationSectionData):
    client = InfluxGTRClient(url=url, token=token, org=organization, bucket_name=bucket)
    contents = client.read_correlation_data(condition)
    return contents


# get df TRC
def get_df_TRC(condition: FacilityData):
    client = InfluxDBClient(url=url, token=token, org=organization)
    query = section_query(bucket, facility=condition.facility,
                          start_date=condition.startTime, end_date=condition.endTime)
    try:
        return execute_query(client, query)
    except Exception as e:
        raise HTTPException(500, str(e))


# get section information by FacilityData
def get_section(condition: FacilityData):
    client = InfluxDBClient(url=url, token=token, org=organization)
    query = section_query(bucket, facility=condition.facility,
                          start_date=condition.startTime, end_date=condition.endTime)
    try:
        return execute_query(client, query)
    except Exception as e:
        raise HTTPException(500, str(e))
