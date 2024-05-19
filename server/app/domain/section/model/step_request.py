from pydantic import BaseModel
from typing import Optional, List


class StepsRequest(BaseModel):
    facility: str
    steps: Optional[List[int]] = None
