from datetime import datetime, timedelta

import warnings
from influxdb_client.client.warnings import MissingPivotFunction

import pandas as pd
from influxdb_client import InfluxDBClient

from config import settings

url = settings.influx_url
token = settings.influx_token
organization = settings.influx_org
bucket = settings.influx_bucket

warnings.simplefilter('ignore', MissingPivotFunction)

# query for factor list
def measurement_query(b: str, measurement: str, start_date: str, end_date: str) -> str:
    return f'''
            from(bucket: "{b}")
            |> range(start: time(v: "{start_date}"), stop: time(v: "{end_date}"))
            |> filter(fn: (r) => r["_measurement"] == "{measurement}") 
            '''
# query for fields time
def fields_time_query(b: str, facility: str, fields, start_date: str, end_date: str) -> str:
    print("fields", fields)
    print("date", start_date, " ", end_date)
    fields_filter = " or ".join([f'r["_field"] == "{field}"' for field in fields])

    return f"""
            from(bucket: "{b}")
            |> range(start: time(v: "{start_date}"), stop: time(v: "{end_date}"))
            |> filter(fn: (r) => r["_measurement"] == "{facility}") 
            |> filter(fn: (r) => {fields_filter})
            """
# query for field time
def field_time_query(b: str, facility: str, field: str, start_date: str, end_date: str) -> str:
    # date string -> date obj
    start_dt = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")

    # calculate window size
    window_size_seconds = (end_dt - start_dt).total_seconds()
    window_size_seconds = 1
    window_size = f"{int(window_size_seconds)}s"  # Flux에서 사용할 수 있는 형태의 문자열로 변환

    return f'''
            from(bucket: "{b}")
                |> range(start: time(v: "{start_date}"), stop: time(v: "{end_date}"))
                |> filter(fn: (r) => r["_measurement"] == "{facility}" and r["_field"] == "{field}")
                |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
            //  |> rename(columns: {{"{field}": "Value"}})
                |> keep(columns: ["_time", "{field}", "P.MF211Ar[sccm]"])
            '''

# query for get section
def section_query(b: str, facility: str, start_date: str, end_date: str) -> str:
    return f'''
            from(bucket: "{b}")
            |> range(start: time(v: "{start_date}"), stop: time(v: "{end_date}"))
            |> filter(fn: (r) => r["_measurement"] == "{facility}")
            |> filter(fn: (r) => r["_field"] == "RcpReq[]" or r["_field"] == "CoatingLayerN[Layers]") 
            
            |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
            |> keep(columns: ["_time", "RcpReq[]", "CoatingLayerN[Layers]"])
            '''

# info facility
def info_measurements_query(b: str) -> str:
    return f"""
            import "influxdata/influxdb/schema"
            schema.measurements(bucket: "{b}")
            """
# info parameter
def info_field_query(b: str, measurement: str) -> str:
    return f"""
            import "influxdata/influxdb/schema"
            schema.fieldKeys(
            bucket: "{b}",
            predicate: (r) => r._measurement == "{measurement}",
            )
            """
# execute query
def execute_query(client: InfluxDBClient, query: str) -> pd.DataFrame:
    df_result = client.query_api().query_data_frame(org=settings.influx_org, query=query)
    df_result.drop(columns=['result', 'table'], inplace=True)
    df_result.rename(columns={"_time": "Time"}, inplace=True)

    return df_result