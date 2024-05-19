from datetime import datetime

from pydantic import BaseModel


class BatchInfo(BaseModel):
    batchName: str
    batchStartTime: str
    batchEndTime: str
    steps: []
    stepsCnt: int
    last_updated: datetime

    class Config:
        arbitrary_types_allowed = True