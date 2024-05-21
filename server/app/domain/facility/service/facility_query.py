import warnings
from datetime import datetime, timedelta

import pandas as pd

from influxdb_client.client.warnings import MissingPivotFunction
from influxdb_client import InfluxDBClient

from config import settings

# settings
url = settings.influx_url
token = settings.influx_token
organization = settings.influx_org
bucket = settings.influx_bucket

# ignore related pivot warnings
warnings.simplefilter('ignore', MissingPivotFunction)

def field_by_time_query(bucket: str, facility: str, field: str, start_date: str = '1970-01-01T00:00:00.0Z',
                        end_date: str = datetime.now().replace(microsecond=0).isoformat() + ".0Z", all: bool = False):
    """
    Query for retrieving the list of field value

    :param bucket: bucket name
    :param facility: measurement name
    :param field: field name
    :param start_date: start time
    :param end_date: end time
    :param all: if True, no down scale
    :return: string for retrieving the list of field value
    """

    if all:
        window_size = 0  # window_size is for down scale
    else:
        end_time = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
        start_time = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
        time_difference = end_time - start_time
        window_size = int(int(time_difference.total_seconds()) / 14400)

    start_date = start_date.replace('Z', '+00:00')
    end_date = end_date.replace('Z', '+00:00')

    base_query = f'''
            from(bucket: "{bucket}")
                |> range(start: time(v: "{start_date}"), stop: time(v: "{end_date}"))
                |> filter(fn: (r) => r["_measurement"] == "{facility}" and r["_field"] == "{field}")
            '''
    window_size_query = f"|> aggregateWindow(every: {window_size}s, fn: mean, createEmpty: false)\n" if window_size != 0 else ""
    select_column_query = '|> keep(columns: ["_time", "_value"])'
    return base_query + window_size_query + select_column_query

def TGLife_time_query(bucket: str, facility: str, num: str, start_date: str, end_date: str):
    """
    Query for retrieving the list of tg life value

    :param bucket: bucket name
    :param facility: measurement name
    :param num: tg life number
    :param start_date: start time
    :param end_date: end time
    :return: string for retrieving the list of tg life value
    """

    return f"""
            from(bucket: "{bucket}")
              |> range(start: time(v: "{start_date}"), stop: time(v: "{end_date}"))
              |> filter(fn: (r) => r["_measurement"] == "{facility}")
              |> filter(fn: (r) => r["_field"] == "P.TG{num}V[V]")
              |> filter(fn: (r) => r.section != "-" and int(v: r.section) < 20)
              |> group(columns: ["section", "TG{num}Life[kWh]_TAG"])
              |> reduce(
                  identity: {{count: 0.0, sum: 0.0, max: 0.0, min: 100000.0, "_TG{num}Life[kWh]": 20000.0}},
                  fn: (r, accumulator) => ({{
                    count: accumulator.count + 1.0,
                    sum: accumulator.sum + r._value,
                    max: if accumulator.max > float(v: r._value) then accumulator.max else float(v: r._value),
                    min: if accumulator.min < float(v: r._value) then accumulator.min else float(v: r._value),
                    "_TG{num}Life[kWh]": if accumulator["_TG{num}Life[kWh]"] < float(v: r["TG{num}Life[kWh]_TAG"]) 
                    then accumulator["_TG{num}Life[kWh]"] else float(v: r["TG{num}Life[kWh]_TAG"])
                  }})
              )
              |> keep(columns: ["_TG{num}Life[kWh]", "section", "count", "sum", "max", "min"])
            """

def TGLife_count_query(bucket: str, facility: str, num: str, start_cnt: str, end_cnt: str):
    """
    Query for retrieving the list of tg life value

    :param bucket: bucket name
    :param facility: measurement name
    :param num: tg life number
    :param start_cnt: start time
    :param end_cnt: end time
    :return: string for retrieving the list of tg life value
    """
    return f"""
            from(bucket: "{bucket}")
              |> range(start: time(v: "1970-01-01T00:00:00.0Z"), stop: time(v: now()))
              |> filter(fn: (r) => r["_measurement"] == "{facility}")
              |> filter(fn: (r) => r["_field"] == "P.TG1V[V]")
              |> filter(fn: (r) => r.section != "-" and int(v: r.section) < 20)
              |> filter(fn: (r) => float(v: r["TG{num}Life[kWh]_TAG"]) > {start_cnt} and float(v: r["TG{num}Life[kWh]_TAG"]) < {end_cnt})
              |> group(columns: ["section", "TG{num}Life[kWh]_TAG"])
              |> reduce(
                  identity: {{count: 0.0, sum: 0.0, max: 0.0, min: 100000.0, "_TG1Life[kWh]": 20000.0}},
                  fn: (r, accumulator) => ({{
                    count: accumulator.count + 1.0,
                    max: if accumulator.max > float(v: r._value) then accumulator.max else float(v: r._value),
                    min: if accumulator.min < float(v: r._value) then accumulator.min else float(v: r._value),
                    sum: accumulator.sum + r._value,
                    "_TG{num}Life[kWh]": if accumulator["_TG{num}Life[kWh]"] < float(v: r["TG{num}Life[kWh]_TAG"]) 
                    then accumulator["_TG{num}Life[kWh]"] else float(v: r["TG{num}Life[kWh]_TAG"])
                  }})
              )
              |> keep(columns: ["_TG{num}Life[kWh]", "count", "sum", "max", "min", "section"])
    """

def measurement_list_query(bucket: str):
    """
    Query for retrieving the list of measurement name
    (ex.
            _value
        0   MASS01
        1   MASS02)

    :param bucket: bucket name
    :return: dataframe that is measurement name list or None if bucket is not specified
    """
    return f"""
            import "influxdata/influxdb/schema"
            schema.measurements(bucket: "{bucket}")
            """

def field_list_query(bucket: str, measurement: str):
    """
    Query for retrieving the list of field name
    (ex.
            _value
        0   BipMode_1[]
        1   BipMode_2[])

    :param bucket: bucket name
    :param measurement: measurement name
    :return: dataframe that is field list or None if not have data in datetime
    """
    return f"""
            import "influxdata/influxdb/schema"
            schema.fieldKeys(
            bucket: "{bucket}",
            predicate: (r) => r._measurement == "{measurement}",
            start: -1y,
            )
            """

def correlation_query(bucket: str, facility: str, fields: list, start_date: str, end_date: str):
    end_time = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
    start_time = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
    time_difference = end_time - start_time
    window_size = int(int(time_difference.total_seconds()) / 14400)
    if window_size == 0:
        window_size = 1

    fields_filter = " or ".join([f'r["_field"] == "{field}"' for field in fields])

    return f'''
            from(bucket: "{bucket}")
            |> range(start: time(v: "{start_date}"), stop: time(v: "{end_date}"))
            |> filter(fn: (r) => {fields_filter})
            |> filter(fn: (r) => r["_measurement"] == "{facility}")
            |> aggregateWindow(every: {window_size}s, fn: mean, createEmpty: false)
            |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
            '''

def execute_query(client: InfluxDBClient, query: str) -> pd.DataFrame | None:
    """
    Execute query on InfluxDB client

    :param client:
    :param query:
    :return: dataframe that executed query
    """
    try:
        df = client.query_api().query_data_frame(org=settings.influx_org, query=query)
        df.drop(columns=['result', 'table'], inplace=True)
        df.rename(columns={"_time": "Time"}, inplace=True)
    except KeyError as e:
        return None

    return df