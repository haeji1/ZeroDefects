from typing import Optional

from pydantic import BaseModel


class GraphQueryData(BaseModel):
    facility: str
    parameter: str
    batchName: Optional[str] = None