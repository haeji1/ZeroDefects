from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class FacilityData(BaseModel):
    facility: str
    parameter: str
    startTime: str
    endTime: str
    batchName: Optional[str] = None
    step: Optional[int] = None


class TGLifeData(BaseModel):
    facility: str
    tgLifeNum: str
    startTime: str = '1970-01-01T00:00:00.0Z'
    endTime: str = datetime.now().replace(microsecond=0).isoformat() + ".0Z"