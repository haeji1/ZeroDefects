from typing import List

from fastapi import HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
from fastapi.responses import JSONResponse
import pandas as pd
from starlette import status

from app.domain.board.model.board import Post, Comment
from app.domain.board.service.board_service import incremental_id
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
    id_list = db.posts.find({}, sort=[("id", -1)]).limit(1)
    list_id = 0
    id_list = list(id_list)  # 커서를 리스트로 변환
    if list(id_list):
        list_id = incremental_id(id_list[0]["id"])
    post.id = list_id
    print(post)
    new_post = db.posts.insert_one(post.dict())

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
async def read_post(post_id: int):
    post = db.posts.find_one({"id": post_id})

    if post is None:
        return JSONResponse(status_code=404, content={"detail": "Post not found"})

    post_data = {
        "id": post["id"],
        "title": post["title"],
        "content": post["content"],
        "nickname": post["nickname"],
        "password": post["password"],
        "comments": [Comment(**comment) for comment in post.get("comments", [])]
    }
    post2 = Post(**post_data)

    return JSONResponse(status_code=200, content=post2.dict())
