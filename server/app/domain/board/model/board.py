from typing import Optional, List

from pydantic import BaseModel


class Comment(BaseModel):
    author: str
    content: str
    password: str


class Post(BaseModel):
    id: int
    title: str
    content: str
    nickname: str
    password: str
    comments: List[Comment] = []


class PostInDB(Post):
    id: str
