from typing import List

import uvicorn
from fastapi import APIRouter, HTTPException
from pymongo import MongoClient

from config import settings
from domain.facility.model.facility_data import FacilityData
from domain.section.model.batch_info import FacilityInfo
from domain.section.service import batch_service
from domain.section.service.batch_service import get_batches_info

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


@section_router.get("/bokeh-section")
def read_section(request_body: List[FacilityData]):
    return batch_service.read_from_section(request_body)
