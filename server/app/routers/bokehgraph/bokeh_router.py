# service
import app.routers.bokehgraph.bokeh_service as bokeh_service

from fastapi import APIRouter
from fastapi.responses import JSONResponse

# bokeh
from bokeh.embed import json_item
from datetime import date, time


# post
from pydantic import BaseModel
from typing import List

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

# df = load_file(file_name)
df = bokeh_service.load_file(file_name)
start = 1120
end = 4948

tg_start = 1026
tg_end = 5687

router = APIRouter(
    prefix="/bokeh",
    tags=["bokeh"]
)

class GraphDataItem(BaseModel):
    facility: str
    parameter: str
    startDate: date
    startTime: time
    endDate: date
    endTime: time


class GraphData(BaseModel):
    graph_data: List[GraphDataItem]


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


@router.post("/graph/data")
async def receive_graph_data(graph_data : GraphData):
    # draw_request_graph(graph_data.graph_data)
    bokeh_service.get_bokeh_data(graph_data.graph_data)
    return graph_data.graph_data