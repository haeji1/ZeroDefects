from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Comment(BaseModel):
    id: int = 0
    author: str
    content: str
    password: str
    date: Optional[datetime] = datetime.now()


class Post(BaseModel):
    id: int = 0
    title: str
    content: str
    nickname: str
    password: str
    comments: List[Comment] = []
    date: Optional[datetime] = datetime.now()
