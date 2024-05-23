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
    type: str
    facility: str
    tgLifeNum: str
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    startCnt: Optional[int] = None
    endCnt: Optional[int] = None


class TGCondition(BaseModel):
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    startCnt: Optional[int] = None
    endCnt: Optional[int] = None


class TGData(BaseModel):
    facility: str
    tgLifeNum: str


class TGLifeModel(BaseModel):
    queryType: str
    queryCondition: TGCondition
    queryData: TGData
