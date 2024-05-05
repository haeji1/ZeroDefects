import uvicorn
from fastapi import APIRouter
from pymongo import MongoClient
from app.models.influx.influx_models import FacilityData
from app.utils.functions.section import get_section_data
from config import settings

url = settings.mongo_furl

# MongoDB client
client = MongoClient(url)
# database name is setting
setting = client["setting"]

section_router = APIRouter(prefix="/api", tags=['section'])


@section_router.post("/section")
async def section(conditon: FacilityData):
    # print('conditon', conditon)
    return {"batches": get_section_data(conditon)}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
