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


from config import settings
from app.domain.facility.model.facility_data import FacilityData
from app.domain.facility.service import facility_query

url = settings.influx_url
token = settings.influx_token
organization = settings.influx_org
bucket = settings.influx_bucket

warnings.simplefilter('ignore', MissingPivotFunction)



def get_facilities_info():
    client = InfluxDBClient(url=url, token=token, org=organization)
    answer_measurements = facility_query.execute_query(client, facility_query.info_measurements_query(b=bucket))

    facilities = defaultdict(list)
    for measurement in answer_measurements['_value']:
        answer_fields = client.query_api().query_data_frame(
            facility_query.info_field_query(b=bucket, measurement=measurement))

        fields = [field for field in answer_fields['_value']]
        facilities[measurement] = fields

    return {'result': dict(facilities)}


# get data
def get_datas(conditions: List[FacilityData]) -> []:
    start_time = time.time()
    facility_list = []
    parameter_list = []
    df_list = []

    client = InfluxDBClient(url=url, token=token, org=organization)
    for condition in conditions:
        query = facility_query.field_time_query(
            b=bucket, facility=condition.facility, field=condition.parameter,
            start_date=condition.startTime, end_date=condition.endTime)

        try:
            facility_list.append(condition.facility)
            parameter_list.append(condition.parameter)
            df_list.append(facility_query.execute_query(client, query))
        except Exception as e:
            raise HTTPException(500, str(e))

    print('time: ', time.time() - start_time)
    return [facility_list, parameter_list, df_list]


# get df TRC
def get_df_TRC(condition: FacilityData):
    client = InfluxDBClient(url=url, token=token, org=organization)
    query = facility_query.section_query(bucket, facility=condition.facility,
                                         start_date=condition.startTime, end_date=condition.endTime)
    try:
        return facility_query.execute_query(client, query)
    except Exception as e:
        raise HTTPException(500, str(e))


# get section information by FacilityData
def get_section(condition: FacilityData):
    client = InfluxDBClient(url=url, token=token, org=organization)
    query = facility_query.section_query(bucket, facility=condition.facility,
                                         start_date=condition.startTime, end_date=condition.endTime)
    try:
        return facility_query.execute_query(client, query)
    except Exception as e:
        raise HTTPException(500, str(e))
