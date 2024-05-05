from pydantic import BaseModel


class BatchAndStepsSection(BaseModel):
    batchName: str
    batchStartTime: str
    batchEndTime: str
    steps: []

    class Config:
        arbitrary_types_allowed = True


# class StepSection(BaseModel):
#     batchName: str
#     batchStartTime: str
#     batchEndTime: str
#     steps: []
#
#     class Config:
#         arbitrary_types_allowed = True


class SectionModel(BaseModel):
    startTime: str
    endTime: str

    class Config:
        arbitrary_types_allowed = True
