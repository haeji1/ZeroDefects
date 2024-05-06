import uvicorn
from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from app.models.section.section_models import FacilityInfo, GraphQueryRequest
from app.utils.functions.section import get_batches_info, get_sections_info
from config import settings

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
    if request_body.queryType == "time":
        sections = []
        for data in request_body.queryData:
            section = {
                "facility": data.facility,
                "batchName": data.batchName,
                "parameter": data.parameter,
                "startTime": request_body.queryCondition.startTime,
                "endTime": request_body.queryCondition.endTime,
            }
            sections.append(section)
        return {"sections": sections}
    elif request_body.queryType == "step":
        sections = get_sections_info(request_body)
        if not sections:
            raise HTTPException(status_code=404, detail="Sections not found")
        return {"sections": sections}
    else:
        raise HTTPException(status_code=404, detail="queryType must be 'time' or 'step'")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
