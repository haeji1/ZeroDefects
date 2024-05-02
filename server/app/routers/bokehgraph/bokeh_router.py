# service
import app.routers.bokehgraph.bokeh_service as bokeh_service
from collections import defaultdict
from typing import List, Dict, Any
from influxdb_client import InfluxDBClient

from fastapi import APIRouter
from fastapi.responses import JSONResponse

# bokeh
from bokeh.embed import json_item

from app.routers.influx.influx_model import FacilityData
from app.routers.influx.influx_utils import influx_list_time_query

router = APIRouter(
    prefix="/bokeh",
    tags=["bokeh"]
)

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
                iso_time = record.get_time().isoformat() # + "Z"
                factor_dictionary['Time'].append(iso_time)
            factor_dictionary[record.get_field()].append(record.get_value())
        flag = False

    return factor_dictionary

@router.post("/read")
async def read_influxdb(conditions: List[FacilityData]):

    # get facility, parameter, df from influxdb
    facility_list, parameter_list, df_list = influx_list_time_query(conditions)
    plots = bokeh_service.draw_dataframe_to_graph(df_list)
    plot_json = [json_item(plot, f"my_plot_{idx}") for idx, plot in enumerate(plots)]

    return JSONResponse(content=plot_json)
