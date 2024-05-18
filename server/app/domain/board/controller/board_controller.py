from typing import List

from fastapi import HTTPException, APIRouter, Body, Depends
from fastapi_pagination import Page, Params, paginate

from app.domain.board.model.User import User
from app.domain.board.model.board import Post, Comment
from app.domain.board.service.comment_service import create_comment_from_db, get_comments_from_db, \
    delete_comment_from_db, update_comment_in_db
from app.domain.board.service.post_service import update_post_from_db, \
    delete_post_from_db, read_post_from_db, get_post_from_db, create_post_from_db
post_router = APIRouter(prefix="/post", tags=['post'])


@post_router.post("/posts")
async def create_post(post: Post):
    return create_post_from_db(post)


@post_router.get("/posts", response_model=Page[Post])
async def get_posts(params: Params = Depends()):
    params.size = 10
    return paginate(list(get_post_from_db()),params)


@post_router.get("/posts/{post_id}")
async def read_post(post_id: int):
    return read_post_from_db(post_id)


@post_router.delete("/posts/{post_id}")
async def delete_post(post_id: int, user_form: User = Body(...)):
    return delete_post_from_db(post_id, user_form.author, user_form.password)


@post_router.put("/posts/{post_id}")
async def update_post(post_id: int, post: Post):
    return update_post_from_db(post_id, post)


@post_router.post("/posts/{post_id}/comments")
async def add_comment(post_id: int, comment: Comment = Body(...)):
    return create_comment_from_db(post_id, comment)


@post_router.get("/posts/{post_id}/comments")
async def get_comments(post_id: int):
    return get_comments_from_db(post_id)


@post_router.delete("/posts/{post_id}/comments/{comment_id}")
async def delete_comment(post_id: int,comment_id: int, user_form: User = Body(...)):
    return delete_comment_from_db(post_id, comment_id, user_form.author, user_form.password)


@post_router.put("/posts/{post_id}/comments/{comment_id}")
async def update_comment(post_id: int, comment_id: int, comment: Comment):
    return update_comment_in_db(post_id, comment_id, comment)
