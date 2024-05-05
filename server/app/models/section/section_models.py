from pydantic import BaseModel


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
