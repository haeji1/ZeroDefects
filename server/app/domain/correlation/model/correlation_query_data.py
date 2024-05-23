from typing import Optional, List

from pydantic import BaseModel


class CorrelationQueryData(BaseModel):
    facility: str
    parameter: List[str]
    batchName: Optional[str] = None
