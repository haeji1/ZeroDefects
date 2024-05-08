from typing import List

from pydantic import BaseModel

from app.domain.section.model.graph_query_condition import GraphQueryCondition
from app.domain.section.model.graph_query_data import GraphQueryData


class GraphQueryRequest(BaseModel):
    queryType: str
    queryCondition: GraphQueryCondition
    queryData: List[GraphQueryData]