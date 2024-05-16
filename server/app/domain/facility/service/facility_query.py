import warnings
from datetime import datetime

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

# query for measurement list
def measurement_query(b: str, measurement: str, start_date: str, end_date: str) -> str:
    return f'''
            from(bucket: "{b}")
            |> range(start: time(v: "{start_date}"), stop: time(v: "{end_date}"))
            |> filter(fn: (r) => r["_measurement"] == "{measurement}") 
            '''

# query fields by time
def fields_by_time_query(b: str, facility: str, fields, start_date: str, end_date: str) -> str:
    fields_filter = " or ".join([f'r["_field"] == "{field}"' for field in fields])

    return f"""
            from(bucket: "{b}")
            |> range(start: time(v: "{start_date}"), stop: time(v: "{end_date}"))
            |> filter(fn: (r) => r["_measurement"] == "{facility}") 
            |> filter(fn: (r) => {fields_filter})
            """

# query field by time
def field_by_time_query(b: str, facility: str, field: str,
                        start_date: str = '1970-01-01T00:00:00.0Z',
                        end_date: str = datetime.now().replace(microsecond=0).isoformat() + ".0Z") -> str:
    end_time = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
    start_time = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
    time_difference = end_time - start_time
    window_size = int(int(time_difference.total_seconds()) / 14400)
    if window_size == 0:
        window_size = 1

    return f'''
            from(bucket: "{b}")
                |> range(start: time(v: "{start_date}"), stop: time(v: "{end_date}"))
                |> filter(fn: (r) => r["_measurement"] == "{facility}" and r["_field"] == "{field}")
                |> group()
                |> sort(columns: ["_time"], desc: false)
                |> aggregateWindow(every: {window_size}s, fn: mean, createEmpty: false)
                |> keep(columns: ["_time", "_value"])
            '''

# query tg_life by num
def TGLife_query(b: str, facility: str, tg_life_num: str, start_date: str, end_date: str, type: str,
                 count: bool) -> str:
    statistics_type = 'None'

    if type == 'AVG':
        statistics_type = 'mean'
    elif type == 'MAX':
        statistics_type = 'max'
    elif type == 'MIN':
        statistics_type = 'min'
    elif type == 'STDDEV':
        statistics_type = 'stddev'

    return f"""
            import "experimental"
            import "join"

            voltage = from(bucket: "{b}")
                |> range(start: time(v: "{start_date}"), stop: time(v: "{end_date}"))
                |> filter(fn: (r) => r["_measurement"] == "{facility}")
                |> filter(fn: (r) => r["_field"] == "P.TG{tg_life_num}V[V]")
                |> group(columns: ["TG{tg_life_num}Life[kWh]_TAG"])
                |> {statistics_type}()

            current = from(bucket: "{b}")
                |> range(start: time(v: "{start_date}"), stop: time(v: "{end_date}"))
                |> filter(fn: (r) => r["_measurement"] == "{facility}")
                |> filter(fn: (r) => r["_field"] == "P.TG{tg_life_num}I[A]")
                |> group(columns: ["TG{tg_life_num}Life[kWh]_TAG"])
                |> {statistics_type}()

            power = from(bucket: "{b}")
                |> range(start: time(v: "{start_date}"), stop: time(v: "{end_date}"))
                |> filter(fn: (r) => r["_measurement"] == "{facility}")
                |> filter(fn: (r) => r["_field"] == "P.TG{tg_life_num}Pwr[kW]")
                |> group(columns: ["TG{tg_life_num}Life[kWh]_TAG"])
                |> {statistics_type}()

            firstjoin = join.tables(
                method: "left",
                left: voltage,
                right: current,
                on: (l, r) => l["TG{tg_life_num}Life[kWh]_TAG"] == r["TG{tg_life_num}Life[kWh]_TAG"],
                as: (l, r) => (
                {{"TG{tg_life_num}Life[kWh]_TAG": l["TG{tg_life_num}Life[kWh]_TAG"],
                "P.TG{tg_life_num}V[V]": l._value, 
                "P.TG{tg_life_num}I[A]": r._value, 
                _start:l._start, _stop:l._stop}}),
            )

            secondjoin = join.tables(
                method: "left",
                left: firstjoin,
                right: power,
                on: (l, r) => l["TG{tg_life_num}Life[kWh]_TAG"] == r["TG{tg_life_num}Life[kWh]_TAG"],
                as: (l, r) => (
                {{"TG{tg_life_num}Life[kWh]_TAG": l["TG{tg_life_num}Life[kWh]_TAG"], 
                "P.TG{tg_life_num}V[V]": l["P.TG{tg_life_num}V[V]"], 
                "P.TG{tg_life_num}I[A]": l["P.TG{tg_life_num}I[A]"], 
                "P.TG{tg_life_num}Pwr[kW]": r._value, 
                _start:l._start, _stop:l._stop}}),
            )
            """ + count_query(b=b, facility=facility, tg_life_num=tg_life_num,
                              start_date=start_date, end_date=end_date, count=count)

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
            start: -1y,
            )
            """

def count_query(b: str, facility: str, tg_life_num: str, start_date: str, end_date: str, count: bool) -> str:
    # query for count value
    if count is True:
        additional_query = f"""
                            count_elements = from(bucket: "{b}")
                                |> range(start: time(v: "{start_date}"), stop: time(v: "{end_date}"))
                                |> filter(fn: (r) => r["_measurement"] == "{facility}")
                                |> filter(fn: (r) => r["_field"] == "P.TG{tg_life_num}V[V]")
                                |> group(columns: ["TG{tg_life_num}Life[kWh]_TAG"])
                                |> count()

                            final_join = join.tables(
                                method: "left",
                                left: secondjoin,
                                right: count_elements,
                                on: (l, r) => l["TG{tg_life_num}Life[kWh]_TAG"] == r["TG{tg_life_num}Life[kWh]_TAG"],
                                as: (l, r) => ({{
                                    "TG{tg_life_num}Life[kWh]_TAG": l["TG{tg_life_num}Life[kWh]_TAG"],
                                    "P.TG1V[V]": l["P.TG{tg_life_num}V[V]"],
                                    "P.TG1I[A]": l["P.TG{tg_life_num}I[A]"],
                                    "P.TG1Pwr[kW]": l["P.TG{tg_life_num}Pwr[kW]"],
                                    "count": r._value,
                                    _start: l._start,
                                    _stop: l._stop
                                }})
                            )

                            final_join
                                |> keep(columns: [
                                "TG{tg_life_num}Life[kWh]_TAG", 
                                "P.TG{tg_life_num}V[V]", 
                                "P.TG{tg_life_num}I[A]", 
                                "P.TG{tg_life_num}Pwr[kW]", 
                                "count"])
                                |> yield(name: "leftJoinResult")
                            """
    else:
        # default additional query
        additional_query = f"""
                            secondjoin
                                |> keep(columns: [
                                "TG{tg_life_num}Life[kWh]_TAG", 
                                "P.TG{tg_life_num}V[V]", 
                                "P.TG{tg_life_num}I[A]", 
                                "P.TG{tg_life_num}Pwr[kW]"])
                                |> yield(name: "TGLife")
                            """

    return additional_query

# execute query
def execute_query(client: InfluxDBClient, query: str) -> pd.DataFrame | None:
    try:
        df_result = client.query_api().query_data_frame(org=settings.influx_org, query=query)
        df_result.drop(columns=['result', 'table'], inplace=True)
        df_result.rename(columns={"_time": "Time"}, inplace=True)
    except Exception as e:
        return None

    return df_result