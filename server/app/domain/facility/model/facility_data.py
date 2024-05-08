from typing import Optional

from pydantic import BaseModel


class FacilityData(BaseModel):
    facility: str
    parameter: str
    startTime: str
    endTime: str
    batchName: Optional[str] = None
    step: Optional[int] = None