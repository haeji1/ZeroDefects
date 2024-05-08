from typing import List

from fastapi import APIRouter

from domain.facility.model.facility_data import FacilityData
from domain.graph.service import graph_service

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
