from typing import List

import uvicorn
from bokeh.embed import json_item
from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from fastapi.responses import JSONResponse

from app.models.influx.influx_models import SectionData
from app.models.section.section_models import FacilityInfo, GraphQueryRequest
from app.service.bokeh.bokeh_service import draw_dataframe_to_graph
from app.utils.functions.influx_functions import get_datas
from app.utils.functions.section import get_batches_info, get_sections_info
from config import settings
from datetime import datetime

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
    return {"batches": batches}


@section_router.post("/draw-graph")
async def draw_graph(request_body: GraphQueryRequest):
    print("=======================")
    print(request_body)
    print("=====queryType======")
    print(request_body.queryType)
    print("=====queryData=======")
    print(request_body.queryData)
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
            print("========sections=======")
            print('sections ', sections)
            graph_type, graph_df = get_datas(sections)
            plots = draw_dataframe_to_graph(graph_type, graph_df)
            plot_json = [json_item(plot, f"my_plot_{idx}") for idx, plot in enumerate(plots)]
            print("=========plot_json_success=======")
            # print(plot_json)
        return JSONResponse(status_code=200, content=plot_json)
    elif request_body.queryType == "step":
        sections = get_sections_info(request_body)
        print("==============sections============")
        print(sections)
        sections_list: List[SectionData] = []
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
        print("======sections_list======")
        print(sections_list)
        graph_type, graph_df = get_datas(sections_list)
        plots = draw_dataframe_to_graph(graph_type, graph_df)
        plot_json = [json_item(plot, f"my_plot_{idx}") for idx, plot in enumerate(plots)]
        print(plot_json)
        # return JSONResponse(status_code=200, content=plot_json)
        if not sections:
            raise HTTPException(status_code=404, detail="Sections not found")
        # return {"sections": sections}
        return JSONResponse(status_code=200, content=plot_json)
    else:
        raise HTTPException(status_code=404, detail="queryType must be 'time' or 'step'")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
