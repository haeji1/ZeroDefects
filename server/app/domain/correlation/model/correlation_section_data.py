from typing import Optional, List

from pydantic import BaseModel


class CorrelationSectionData(BaseModel):
    facility: str
    batchName: Optional[str] = None
    parameter: List[str]
    startTime: str
    endTime: str