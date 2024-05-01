# service
import os
from collections import defaultdict
from http.client import HTTPException
from typing import List, Dict, Any

import pandas as pd
from influxdb_client import InfluxDBClient
from pydantic import BaseModel

import app.routers.bokehgraph.bokeh_service as bokeh_service

from fastapi import APIRouter
from fastapi.responses import JSONResponse

# bokeh
from bokeh.embed import json_item

file_name = "F1492-ExhaustLog-240323-011325.CSV"
column = "No1_P[kW]"
columns = ["No1_P[kW]","No2_P[kW]","No4_P[kW]","No5_P[kW]"
    ,"No6_P1_Fwd[kW]","No6_P2_Fwd[kW]","No6_P3_Fwd[kW]", "No6_P4_Fwd[kW]"
    ,"No6_A1[sccm]", "No6_O1[sccm]","No6_O2[sccm]","No6_N1[sccm]"
    ,"No1_A1[sccm]","No1_A2[sccm]","No1_A3[sccm]","No1_A4[sccm]"
    ,"No2_A1[sccm]","No2_A2[sccm]","No2_A3[sccm]","No2_A4[sccm]"
    ,"No4_A1[sccm]","No4_A2[sccm]","No4_A3[sccm]","No4_A4[sccm]"
    ,"No5_A1[sccm]","No5_A2[sccm]","No5_A3[sccm]","No5_A4[sccm]"]

tg_file_name = "F1508-ExhaustLog-240412-012855.CSV"
tg_columns = ["P.TG1Pwr[kW]","P.MF211Ar[sccm]","P.MF212Ar[sccm]","P.MF213Ar[sccm]","P.MF214Ar[sccm]"
    ,"P.TG2Pwr[kW]","P.MF221Ar[sccm]","P.MF222Ar[sccm]","P.MF223Ar[sccm]","P.MF224Ar[sccm]"
    ,"P.TG4Pwr[kW]","P.MF241Ar[sccm]","P.MF242Ar[sccm]","P.MF243Ar[sccm]","P.MF244Ar[sccm]"
    ,"P.TG5Pwr[kW]","P.MF251Ar[sccm]","P.MF252Ar[sccm]","P.MF253Ar[sccm]","P.MF254Ar[sccm]"
    ,"P.Icp1PwrFwd[kW]","P.Icp2PwrFwd[kW]","P.Icp3PwrFwd[kW]","P.Icp4PwrFwd[kW]"
    ,"P.MF207Ar[sccm]","P.MF208O2[sccm]","P.MF209O2[sccm]","P.MF210N2[sccm]"]


df = bokeh_service.load_file(file_name)
start = 1120
end = 4948

tg_start = 1026
tg_end = 5687

router = APIRouter(
    prefix="/bokeh",
    tags=["bokeh"]
)


@router.get("/draw/graph")
async def draw_graph_endpoint():
    plot = bokeh_service.draw_graph(column, start, end)
    plot_json = json_item(plot, "my_plot")
    return JSONResponse(content=plot_json)

@router.get("/draw/all-graph")
async def draw_graph_endpoint():
    plots = bokeh_service.draw_all_graph(columns, start, end)
    plot_json = [json_item(plot, f"my_plot_{idx}") for idx, plot in enumerate(plots)]
    return JSONResponse(content=plot_json)

@router.get("/draw/all/tg-graph")
async def draw_graph_endpoint():
    plots = bokeh_service.draw_all_tg_graph(df, tg_start, tg_end)
    plot_json = [json_item(plot, f"my_plot_{idx}") for idx, plot in enumerate(plots)]
    return JSONResponse(content=plot_json)

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
class FacilityData(BaseModel):
    facility: str
    parameter: str
    startTime: str
    endTime: str
@router.get("/read")
async def read_influxdb(conditions: List[FacilityData]):

    url = os.getenv("INFLUXDB_URL")
    token = os.getenv("INFLUXDB_TOKEN")
    organization = os.getenv("INFLUXDB_ORGANIZATION")
    bucket = os.getenv("INFLUXDB_BUCKET")

    results = []
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
            results.append(factor_dictionary)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    print('facility_list', facility_list)
    print('prameter_list', prameter_list)
    print('df_list', df_list)
    # facility_list, parameter_list, df_list를 활용해서 bokeh 그리고 return 하면돼

    return {'result': results}