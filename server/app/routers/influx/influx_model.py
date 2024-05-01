from pydantic import BaseModel

class FacilityData(BaseModel):
    facility: str
    parameter: str
    startTime: str
    endTime: str