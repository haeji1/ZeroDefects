from pydantic import BaseModel


class BatchInfo(BaseModel):
    batchName: str
    batchStartTime: str
    batchEndTime: str
    steps: []

    class Config:
        arbitrary_types_allowed = True