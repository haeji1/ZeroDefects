import os
from collections import defaultdict
import time
from datetime import datetime, timedelta
from http.client import HTTPException
from typing import List, Dict, Any

import warnings
from influxdb_client.client.warnings import MissingPivotFunction

import pandas as pd
from influxdb_client import InfluxDBClient

from app.domain.facility.model.facility_data import FacilityData
from app.domain.facility.service.facility_query import section_query, execute_query, field_by_time_query, info_field_query, \
    info_measurements_query
from app.domain.section.model.section_data import SectionData
from config import settings

url = settings.influx_url
token = settings.influx_token
organization = settings.influx_org
bucket = settings.influx_bucket

warnings.simplefilter('ignore', MissingPivotFunction)

# --------- functions --------- #

def get_facilities_info():
    client = InfluxDBClient(url=url, token=token, org=organization)
    answer_measurements = execute_query(client, info_measurements_query(b=bucket))

    facilities = defaultdict(list)
    for measurement in answer_measurements['_value']:
        answer_fields = client.query_api().query_data_frame(info_field_query(b=bucket, measurement=measurement))

        fields = [field for field in answer_fields['_value']]
        facilities[measurement] = fields

    return {'result': dict(facilities)}

# get data
def get_datas(conditions: List[SectionData]):
    client = InfluxDBClient(url=url, token=token, org=organization, timeout=1200000)
    result_df: [pd.DataFrame] = []

    for condition in conditions:
        query = field_by_time_query(
                        b=bucket, facility=condition.facility, field=condition.parameter,
                        start_date=condition.startTime, end_date=condition.endTime)
        try:
            query_s = time.time()
            df = execute_query(client, query)
            print('query time ', time.time() - query_s)

            if df is None:
                continue
            df.rename(
                columns={'_value': f'{condition.facility}-{condition.parameter}'},
                inplace=True)

            result_df.append(df)
        except Exception as e:
            raise HTTPException(500, str(e))

    return result_df
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


def get_measurement_code(input):
    mapping = {
        'F1492': 'MASS01',
        'F1494': 'MASS02',
        'F1495': 'MASS04',
        'F1493': 'MASS05',
        'F1500': 'MASS06',
        'F1496': 'MASS07',
        'F1497': 'MASS08',
        'F1498': 'MASS09',
        'F1502': 'MASS10',
        'F1503': 'MASS11',
        'F1501': 'MASS12',
        'F1504': 'MASS13',
        'F1505': 'MASS14',
        'F1507': 'MASS18',
        'F1508': 'MASS22',
    }

    return mapping.get(input, "unknown")