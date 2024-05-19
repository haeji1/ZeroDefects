from typing import Optional, List

from pydantic import BaseModel


class GraphQueryCondition(BaseModel):
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    step: Optional[List[int]] = None
