from typing import List, Optional
from pprint import pprint
import uvicorn
from datetime import datetime, timedelta

from bokeh.embed import json_item
from fastapi import APIRouter, HTTPException, Body
from pymongo import MongoClient
from starlette.responses import JSONResponse

from app.domain.facility.service.facility_function import get_datas
from app.domain.graph.service.draw_service import draw_dataframe_to_graph
from app.domain.section.model.faciltiy_info import FacilityInfo
from app.domain.section.model.graph_query_request import GraphQueryRequest
from app.domain.section.model.section_data import SectionData
from app.domain.section.model.step_data import StepData
from app.domain.section.model.step_request import StepsRequest
from config import settings

from app.domain.section.service.batch_service import get_batches_info, get_sections_info, \
    get_steps_info, extract_step_times, get_step_info_using_facility_name_on_mongoDB

url = settings.mongo_furl

# MongoDB client
client = MongoClient(url)
# database name is setting
setting = client["setting"]

section_router = APIRouter(prefix="/api", tags=['section'])


@section_router.post("/batches")
async def get_batches(facility: FacilityInfo):
    batches_info = get_batches_info(facility)
    if not batches_info:
        raise HTTPException(status_code=404, detail="Batches not found")
    return {"batches": batches_info}


@section_router.post("/steps")
async def get_steps(request: StepsRequest):
    steps_info = get_steps_info(StepsRequest(facility=request.facility, steps=request.steps))
    if not steps_info:
        raise HTTPException(status_code=404, detail="Steps not found")
    return {"steps": steps_info}


# @section_router.get("/bokeh-section")
# def read_section(request_body: List[FacilityData]):
#     return batch_service.read_from_section(request_body)


@section_router.post("/draw-graph")
async def draw_graph(request_body: GraphQueryRequest):
    # pprint(request)
    # print("request_body", request_body)
    batch_name_list = []
    steps_times_info = []
    # get_step_info_using_facility_name_on_mongoDB(request_body)
    if request_body.queryType == "time":
        sections: List[SectionData] = []
        
        # 표준시로 변경
        start_time = datetime.strptime(request_body.queryCondition.startTime, "%Y-%m-%dT%H:%M:%S.%fZ")
        start_time += timedelta(hours=9)
        start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        end_time = datetime.strptime(request_body.queryCondition.endTime, "%Y-%m-%dT%H:%M:%S.%fZ")
        end_time += timedelta(hours=9)
        end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        for s in request_body.queryData:
            sections.append(SectionData(
                facility=s.facility,
                batchName=s.batchName,
                parameter=s.parameter,
                startTime=start_time,
                endTime=end_time
            ))

        graph_df = get_datas(sections)
        plots = draw_dataframe_to_graph("time", graph_df, steps_times_info, batch_name_list)
        plot_json = [json_item(plot, f"my_plot_{idx}") for idx, plot in enumerate(plots)]
        return JSONResponse(status_code=200, content=plot_json)

    elif request_body.queryType == "step":
        request = get_step_info_using_facility_name_on_mongoDB(request_body)
        for query_data in request_body.queryData:
            batch_name = query_data.batchName
            batch_name_list.append(batch_name)
        # setting_value_of_steps = get_step_info_using_facility_name_on_mongoDB(request_body)
        sections = get_sections_info(request_body)
        sections_list: List[SectionData] = []

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
        plots = draw_dataframe_to_graph("step", graph_df, step_times, batch_name_list, request)
        plot_json = [json_item(plot, f"my_plot_{idx}") for idx, plot in enumerate(plots)]
        # toggle_json = [json_item(toggle, f"my_toggle_{idx}") for idx, toggle in enumerate(toggles)]

        # combined_json = plot_json + toggle_json
        # print("======combined_json=======")
        # print(combined_json)


        if not sections:
            raise HTTPException(status_code=404, detail="Sections not found")
        return JSONResponse(status_code=200, content=plot_json)

    else:
        raise HTTPException(status_code=404, detail="queryType must be 'time' or 'step'")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
