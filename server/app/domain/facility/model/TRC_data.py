from pydantic import BaseModel


class TRCData(BaseModel):
    facility: str
    startTime: str
    endTime: str