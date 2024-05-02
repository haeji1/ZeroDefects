from pydantic import BaseModel

class Cycle(BaseModel):
    cycle_name: str
    cycle_start_time: str
    cycle_end_time: str

    class Config:
        arbitrary_types_allowed = True

class CycleSection(BaseModel):
    cycle_name: str
    cycle_start_time: str
    cycle_end_time: str
    steps: []

    class Config:
        arbitrary_types_allowed = True

class SectionModel(BaseModel):
    start_time: str
    end_time: str

    class Config:
        arbitrary_types_allowed = True