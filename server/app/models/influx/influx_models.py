from typing import Optional

from pydantic import BaseModel


class FacilityData(BaseModel):
    facility: str
    parameter: str
    startTime: str
    endTime: str
    cycleName: Optional[str] = None
    step: Optional[int] = None

class TRCData(BaseModel):
    facility: str
    startTime: str
    endTime: str

class SectionData(BaseModel):
    facility: str
    batchName: Optional[str] = None
    parameter: str
    startTime: str
    endTime: str