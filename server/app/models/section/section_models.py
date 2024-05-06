from pydantic import BaseModel
from typing import Optional, List


class BatchInfo(BaseModel):
    batchName: str
    batchStartTime: str
    batchEndTime: str
    steps: []

    class Config:
        arbitrary_types_allowed = True


class FacilityInfo(BaseModel):
    facility: str

    class Config:
        arbitrary_types_allowed = True


class GraphQueryCondition(BaseModel):
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    step: Optional[List[int]] = None


class GraphQueryData(BaseModel):
    facility: str
    parameter: str
    batchName: Optional[str] = None


class GraphQueryRequest(BaseModel):
    queryType: str
    queryCondition: GraphQueryCondition
    queryData: List[GraphQueryData]
