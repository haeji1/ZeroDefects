# service
import app.service.bokeh.bokeh_service as bokeh_service
from collections import defaultdict
from typing import List, Dict, Any
from influxdb_client import InfluxDBClient

from fastapi import APIRouter
from fastapi.responses import JSONResponse

# bokeh
from bokeh.embed import json_item
import json

from app.models.influx.influx_models import FacilityData
from app.utils.functions.influx_functions import get_datas

##############################
import os
from dotenv import load_dotenv
from pymongo import MongoClient
load_dotenv()
url = os.getenv('MONGO_FURL')

# MongoDB client
client = MongoClient(url)
# database name is setting
section = client["section"]

mongo_router = APIRouter(prefix="/facility", tags=['section'])
##############################

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
                iso_time = record.get_time().isoformat()
                factor_dictionary['Time'].append(iso_time)
            factor_dictionary[record.get_field()].append(record.get_value())
        flag = False

    return factor_dictionary

@router.post("/read")
async def read_influxdb(conditions: List[FacilityData]):

    # get facility, parameter, df from influxdb
    graph_type, graph_df = get_datas(conditions)
    plots = bokeh_service.draw_dataframe_to_graph(graph_type, graph_df)
    plot_json = [json_item(plot, f"my_plot_{idx}") for idx, plot in enumerate(plots)]

    return JSONResponse(content=plot_json)

@router.post("/read/single/line")
async def get_single_data_line(conditions: List[FacilityData]):

    facility_list, parameter_list, df_list = get_datas(conditions)
    bokeh_service.draw_single_line(df_list[0], facility_list[0])
    print("============router================")

    x_data, y_data, facility = bokeh_service.draw_single_line(df_list[0], facility_list[0])
    # x_data, facility = bokeh_service.draw_single_line(df_list[0], facility_list[0])

    x_data = [str(timestamp) for timestamp in x_data]

    response_data = {
        "x_data": x_data,
        "y_data":  y_data,
        "facility": facility
    }
    print("===========response_data=========")
    # print(JSONResponse(content=response_data))
    return JSONResponse(content=response_data)

@router.post("/read/multi/line")
async def get_multi_data_line(conditions: List[FacilityData]):

    facility_list, parameter_list, df_list = get_datas(conditions)
    bokeh_service.draw_multi_line(df_list, facility_list)

    print("============router================")

    x_data_list, y_data_list, facility_list = bokeh_service.draw_multi_line(df_list, facility_list)

    x_data_list = [[str(timestamp) for timestamp in x_data] for x_data in x_data_list]

    response_data = {
        "x_data_list": x_data_list,
        "y_data_list": y_data_list,
        "facility_list": facility_list
    }

    print("===========response_data=========")
    print(JSONResponse(content=response_data))
    return JSONResponse(content=response_data)


@router.get("/bokeh-section")
def read_section(request_body: List[FacilityData]):
    results = []
    for item in request_body:
        collection_name = item['facility']  # collection 이름은 facility 값
        cycle_name = item['cycleName']
        step = item.get('step')  # step이 None일 수도 있으므로 get 메소드 사용

        collection = section[collection_name]  # 해당 facility의 컬렉션 선택

        # cycle_name이 있는 경우
        if cycle_name:
            cycle_query = {"cycles.cycle_name": cycle_name}
            cycle_data = collection.find_one(cycle_query)

            if cycle_data:
                for cycle in cycle_data['cycles']:
                    if cycle['cycle_name'] == cycle_name:
                        if step is None:  # step이 None이면 cycle의 시간 정보를 가져옴
                            results.append({
                                "cycle_start_time": cycle['cycle_start_time'],
                                "cycle_end_time": cycle['cycle_end_time']
                            })
                        else:  # step이 지정된 경우 해당 step의 시간 정보를 가져옴
                            step_key = f"step{step}"
                            for step_item in cycle['steps']:
                                if step_key in step_item:
                                    results.append(step_item[step_key])
                                    break
                        break

    return JSONResponse(status_code=200, content=results)