import os
from collections import defaultdict
from http.client import HTTPException
from typing import List, Dict, Any

import pandas as pd
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient

from app.routers.bokehgraph.bokeh_router import FacilityData

load_dotenv()

url = os.getenv('INFLUXDB_URL')
token = os.getenv('INFLUXDB_TOKEN')
organization = os.getenv('INFLUXDB_ORG')
bucket = os.getenv('INFLUXDB_BUCKET')

def influxdb_parameters_query(b: str, facility: str, fields, start_date: str, end_date: str) -> str:
    print("fields", fields)
    print("date", start_date, " ", end_date)
    fields_filter = " or ".join([f'r["_field"] == "{field}"' for field in fields])

    return f"""
            from(bucket: "{b}")
            |> range(start: time(v: "{start_date}"), stop: time(v: "{end_date}"))
            |> filter(fn: (r) => r["_measurement"] == "{facility}") 
            |> filter(fn: (r) => {fields_filter})
            """
def influxdb_parameter_query(b: str, facility: str, field: str, start_date: str, end_date: str) -> str:
    return f'''
            from(bucket: "{b}")
            |> range(start: time(v: "{start_date}"), stop: time(v: "{end_date}"))
            |> filter(fn: (r) => r["_measurement"] == "{facility}" and r["_field"] == "{field}") 
            '''
def execute_query(client: InfluxDBClient, org: str, query: str) -> List[Dict[str, Any]]:
    query_api = client.query_api()
    result = query_api.query(org=org, query=query)
    factor_dictionary = defaultdict(list)
    flag = True
    for records in result:
        for record in records:
            if flag:
                iso_time = record.get_time().isoformat() + "Z"
                factor_dictionary['Time'].append(iso_time)
            factor_dictionary[record.get_field()].append(record.get_value())
        flag = False

    return factor_dictionary
def influx_list_query(conditions: List[FacilityData]) -> []:
    facility_list = []
    prameter_list = []
    df_list = []

    client = InfluxDBClient(url=url, token=token, org=organization)
    for condition in conditions:
        query = influxdb_parameter_query(
            bucket, condition.facility, condition.parameter, condition.startTime, condition.endTime)

        try:
            factor_dictionary = execute_query(client, organization, query)
            df = pd.DataFrame(factor_dictionary)
            df_list.append(df)
            facility_list.append(condition.facility)
            prameter_list.append(condition.parameter)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return [facility_list, prameter_list, df_list]