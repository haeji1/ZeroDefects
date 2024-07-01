from fastapi import UploadFile, File
from typing import List

import warnings

from influxdb_client.client.warnings import MissingPivotFunction

from app.domain.correlation.model.correlation_section_data import CorrelationSectionData
from app.domain.facility.model.facility_data import TGLifeData, RequestTGLifeInfo
from app.domain.facility.service.influx_client import InfluxGTRClient
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
    contents = client.read_facility_info()
    return contents


# get data
def get_datas(conditions: List[SectionData], all: bool = False):
    client = InfluxGTRClient(url=url, token=token, org=organization, bucket_name=bucket)
    contents = client.read_parameter_df(conditions, isWindowScale=all)
    return contents

def get_TG_cycles_info(condition: RequestTGLifeInfo):
    client = InfluxGTRClient(url=url, token=token, org=organization, bucket_name=bucket)
    contents = client.read_TGLife_cycles_info(condition)
    return contents

def get_TG_datas(conditions: [TGLifeData]):
    client = InfluxGTRClient(url=url, token=token, org=organization, bucket_name=bucket)
    contents = client.read_TGLife_df_list(conditions)
    return contents

# def get_TG_datas(condition: TGLifeData):
#     client = InfluxGTRClient(url=url, token=token, org=organization, bucket_name=bucket)
#     contents = client.read_TGLife_df_list(condition)
#     return contents


def get_correlation_datas(condition: CorrelationSectionData):
    client = InfluxGTRClient(url=url, token=token, org=organization, bucket_name=bucket)
    contents = client.read_correlation_data(condition)
    return contents