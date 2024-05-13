from typing import List

from fastapi import HTTPException, APIRouter
from pymongo import MongoClient
from fastapi.responses import JSONResponse
import pandas as pd
from starlette import status

from app.domain.board.model.board import Post
from app.domain.facility.service.facility_function import get_measurement_code
from config import settings

post_router = APIRouter(prefix="/post", tags=['post'])

url = settings.mongo_furl

# MongoDB client
client = MongoClient(url)
# database name is setting
db = client["post"]


@post_router.post("/posts")
async def create_post(post: Post):
    new_post = db.posts.insert_one(post.dict())
    id_list = db.posts.find().sort("id", -1).limit(1)
    id = 0
    if not list(id_list):
        id = 0
    if new_post.inserted_id:
        return {"message": "Post created successfully."}  # JSONResponse 대신 직접 반환
    else:
        return JSONResponse(content={"message": "Failed to create post."}, status_code=status.HTTP_400_BAD_REQUEST)


@post_router.get("/posts", response_model=List[Post])
async def get_posts():
    posts = db.posts.find()
    a = db.posts.find().sort("id", -1).limit(1)
    print(list(a))
    return posts


# 특정 게시글 조회 API
@post_router.get("/posts/{post_id}")
async def read_post(post_id: str):
    post = db.posts.find_one({"_id": post_id})
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post