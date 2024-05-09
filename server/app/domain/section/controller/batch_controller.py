from typing import List

import uvicorn
from datetime import datetime

from bokeh.embed import json_item
from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from starlette.responses import JSONResponse

from app.domain.facility.service.facility_function import get_datas
from app.domain.graph.service.draw_service import draw_dataframe_to_graph
from app.domain.section.model.faciltiy_info import FacilityInfo
from app.domain.section.model.graph_query_request import GraphQueryRequest
from app.domain.section.model.section_data import SectionData
from config import settings

from app.domain.section.service.batch_service import get_batches_info, get_sections_info

url = settings.mongo_furl

# MongoDB client
client = MongoClient(url)
# database name is setting
setting = client["setting"]

section_router = APIRouter(prefix="/api", tags=['section'])


@section_router.post("/batches")
async def get_batches(facility: FacilityInfo):
    batches = get_batches_info(facility)
    if not batches:
        raise HTTPException(status_code=404, detail="Batches not found")
    return {"batches": get_batches_info(facility)}


# @section_router.get("/bokeh-section")
# def read_section(request_body: List[FacilityData]):
#     return batch_service.read_from_section(request_body)


@section_router.post("/draw-graph")
async def draw_graph(request_body: GraphQueryRequest):
    end_time_list = []
    # print("request_body", request_body)
    # print("==========queryType=====")
    # print(request_body.queryType)
    print("===========queryData=======")
    print(request_body.queryType)
    if request_body.queryType == "time":
        sections: List[SectionData] = []
        for s in request_body.queryData:
            sections.append(SectionData(
                facility=s.facility,
                batchName=s.batchName,
                parameter=s.parameter,
                startTime=request_body.queryCondition.startTime,
                endTime=request_body.queryCondition.endTime
            ))
        print("================================")
        graph_df = get_datas(sections)
        print("============graph_df=================")
        print(graph_df)
        print(end_time_list)
        plots = draw_dataframe_to_graph("time", graph_df,end_time_list)
        plot_json = [json_item(plot, f"my_plot_{idx}") for idx, plot in enumerate(plots)]
        return JSONResponse(status_code=200, content=plot_json)
    elif request_body.queryType == "step":
        print("=============")
        sections = get_sections_info(request_body)
        print("==========sections==========")
        print(sections)
        sections_list: List[SectionData] = []
        # print("sections", sections)
        for s in sections:
            s['startTime'] = datetime.strptime(s['startTime'], '%Y-%m-%d %H:%M:%S')
            s['startTime'] = s['startTime'].strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            s['endTime'] = datetime.strptime(s['endTime'], '%Y-%m-%d %H:%M:%S')
            s['endTime'] = s['endTime'].strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            sections_list.append(SectionData(
                facility=s['facility'],
                batchName=s['batchName'],
                parameter=s['parameter'],
                startTime=s['startTime'],
                endTime=s['endTime']
            ))
            end_time_list.append(s['endTime'])
        #     print("============endtimelist============")
        # print(end_time_list)
        graph_df = get_datas(sections_list)
        plots = draw_dataframe_to_graph("step", graph_df, end_time_list)
        plot_json = [json_item(plot, f"my_plot_{idx}") for idx, plot in enumerate(plots)]

        if not sections:
            raise HTTPException(status_code=404, detail="Sections not found")
        return JSONResponse(status_code=200, content=plot_json)
    else:
        raise HTTPException(status_code=404, detail="queryType must be 'time' or 'step'")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
