from pydantic import BaseModel


class User(BaseModel):
    author: str
    password: str
