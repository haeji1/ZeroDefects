from typing import Optional

from pydantic import BaseModel


class SectionData(BaseModel):
    facility: str
    batchName: Optional[str] = None
    parameter: str
    startTime: str
    endTime: str