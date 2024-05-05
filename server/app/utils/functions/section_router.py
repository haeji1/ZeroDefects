import uvicorn
from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from app.models.section.section_models import FacilityInfo
from app.utils.functions.section import get_batches_info
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
    return {"batches": get_batches_info(facility)}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
