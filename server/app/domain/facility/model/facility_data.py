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
    startTime: str
    endTime: str


class TGCondition(BaseModel):
    startTime: str = Optional[str]
    endTime: str = Optional[str]
    startCnt: Optional[str]
    endCnt: Optional[str]


class TGData(BaseModel):
    facility: str
    tgLifeNum: str


class TGLifeModel(BaseModel):
    queryType: str
    queryCondition: TGCondition
    queryData: TGData
