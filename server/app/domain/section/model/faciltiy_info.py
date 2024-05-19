from pydantic import BaseModel


class FacilityInfo(BaseModel):
    facility: str

    class Config:
        arbitrary_types_allowed = True