from pydantic import BaseModel
from typing import List


class BatchAndSteps(BaseModel):
    facility: str
    batchName: str
    steps: List[int]
