from typing import List

from pydantic import BaseModel


class Comment(BaseModel):
    id: int = 0
    author: str
    content: str
    password: str


class Post(BaseModel):
    id: int = 0
    title: str
    content: str
    nickname: str
    password: str
    comments: List[Comment] = []
