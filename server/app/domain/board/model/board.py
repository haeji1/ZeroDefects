from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Comment(BaseModel):
    id: int = 0
    author: str
    content: str
    password: str
    date: Optional[str] = str(datetime.now())


class Post(BaseModel):
    id: int = 0
    title: str
    content: str
    author: str
    password: str
    graphData: Optional[list] = None
    comments: List[Comment] = []
    date: Optional[str] = str(datetime.now())
