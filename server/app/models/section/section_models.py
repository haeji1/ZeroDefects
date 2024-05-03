from pydantic import BaseModel

class Cycle(BaseModel):
    cycleName: str
    cycleStartTime: str
    cycleEndTime: str

    class Config:
        arbitrary_types_allowed = True

class CycleSection(BaseModel):
    cycleName: str
    cycleStartTime: str
    cycleEndTime: str
    steps: []

    class Config:
        arbitrary_types_allowed = True

class SectionModel(BaseModel):
    startTime: str
    endTime: str

    class Config:
        arbitrary_types_allowed = True