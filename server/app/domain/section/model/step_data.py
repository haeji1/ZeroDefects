from pydantic import BaseModel
from typing import Dict, Any


class StepData(BaseModel):
    facility: str
    batchName: str
    stepsTime: Dict[str, Any]
