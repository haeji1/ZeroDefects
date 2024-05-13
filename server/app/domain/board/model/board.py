from typing import Optional, List, Any
from bson import ObjectId
from pydantic import BaseModel, Field

class Comment(BaseModel):
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