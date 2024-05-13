from typing import List

from fastapi import HTTPException, APIRouter

from app.domain.board.model.board import Post
from app.domain.board.service.board_service import update_post_from_db, \
    delete_post_from_db, read_post_from_db, get_post_from_db, create_post_from_db

post_router = APIRouter(prefix="/post", tags=['post'])


@post_router.post("/posts")
async def create_post(post: Post):
    return create_post_from_db(post)


@post_router.get("/posts", response_model=List[Post])
async def get_posts():
    return get_post_from_db()


@post_router.get("/posts/{post_id}")
async def read_post(post_id: int):
    return read_post_from_db(post_id)


@post_router.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    return delete_post_from_db(post_id)


@post_router.put("/posts/{post_id}")
async def update_post(post_id: int, post: Post):
    return update_post_from_db(post_id, post)