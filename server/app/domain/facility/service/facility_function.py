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
from app.domain.facility.service.facility_query import section_query, execute_query, field_time_query, info_field_query, \
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
def get_datas(conditions: List[SectionData]) -> []:
    start_time = time.time()
    result_df = pd.DataFrame()
    client = InfluxDBClient(url=url, token=token, org=organization)

    # conditions length == 1
    if len(conditions) == 1:
        query = field_time_query(
            b=bucket, facility=conditions[0].facility, field=conditions[0].parameter,
            start_date=conditions[0].startTime, end_date=conditions[0].endTime)
        try:
            result_df = execute_query(client, query)
            result_df.rename(columns={f'{conditions[0].parameter}': f'{conditions[0].facility}_{conditions[0].parameter}'}, inplace=True)
        except Exception as e:
            raise HTTPException(500, str(e))

    # conditions length > 1
    if len(conditions) > 1:
        for condition in conditions:
            query = field_time_query(
                b=bucket, facility=condition.facility, field=condition.parameter,
                start_date=condition.startTime, end_date=condition.endTime)

            try:
                result_df['Time'] = execute_query(client, query)[['Time']]
            except Exception as e:
                print(e)

            try:
                result_df[f'{condition.facility}_{condition.parameter}'] = execute_query(client, query)[[condition.parameter]]
                # df_list.append(df)
            except Exception as e:
                raise HTTPException(500, str(e))

    print('time: ', time.time() - start_time)
    return ["step", result_df]
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
