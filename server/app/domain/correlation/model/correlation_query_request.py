from typing import List

from pydantic import BaseModel

from app.domain.correlation.model.correlation_query_condition import CorrelationQueryCondition
from app.domain.correlation.model.correlation_query_data import CorrelationQueryData


class CorrelationQueryRequest(BaseModel):
    queryType: str
    queryCondition: CorrelationQueryCondition
    queryData: List[CorrelationQueryData]