from typing import List

from bokeh.embed import json_item
from fastapi import APIRouter, HTTPException
from datetime import datetime

from starlette.responses import JSONResponse

from app.domain.facility.model.facility_data import FacilityData
from app.domain.facility.service.facility_function import get_datas
from app.domain.graph.service import graph_service
from app.domain.graph.service.draw_service import draw_dataframe_to_graph, draw_detail_section_graph
from app.domain.section.model.graph_query_request import GraphQueryRequest
from app.domain.section.model.section_data import SectionData
from app.domain.section.model.step_data import StepData
from app.domain.section.service.batch_service import get_sections_info, extract_step_times

graph_router = APIRouter(
    prefix="/bokeh",
    tags=["bokeh"]
)


@graph_router.post("/read")
async def read_influxdb(conditions: List[FacilityData]):
    return graph_service.read_from_influxdb(conditions)


@graph_router.get("/bokeh-section")
def read_section(request_body: List[FacilityData]):
    return graph_service.read_from_section(request_body)

@graph_router.post("/draw/section-graph")
async def draw_graph(request_body: GraphQueryRequest):
    # setting_value_of_steps = get_step_info_using_facility_name_on_mongoDB(request_body)
    steps_times_info = []
    sections = get_sections_info(request_body)
    sections_list: List[SectionData] = []
    print("====================sections====================")
    print(sections)
    print("====================sections=====================")
    for s in sections:
        s['startTime'] = datetime.strptime(s['startTime'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        s['endTime'] = datetime.strptime(s['endTime'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        sections_list.append(SectionData(
            facility=s['facility'],
            batchName=s['batchName'],
            parameter=s['parameter'],
            startTime=s['startTime'],
            endTime=s['endTime']
        ))
        steps_times_info.append(StepData(
            facility=s['facility'],
            batchName=s['batchName'],
            stepsTime=s['stepsTimes']
        ))

    step_times = extract_step_times(steps_times_info)
    graph_df = get_datas(sections_list)
    # plots = draw_dataframe_to_graph("step", graph_df, step_times)
    plots = draw_detail_section_graph(graph_df, step_times)
    plot_json = [json_item(plot, f"my_plot_{idx}") for idx, plot in enumerate(plots)]


    if not sections:
        raise HTTPException(status_code=404, detail="Sections not found")
    return JSONResponse(status_code=200, content=plot_json)