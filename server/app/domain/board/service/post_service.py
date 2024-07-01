from fastapi import HTTPException
from pymongo import MongoClient
from starlette import status

from app.domain.board.model.board import Post, Comment
from config import settings
from fastapi.responses import JSONResponse

url = settings.mongo_furl

# MongoDB client
client = MongoClient(url)
# database name is setting
db = client["post"]


def incremental_id(id):
    return id + 1


def post_to_post2(post: Post):
    post_data = {
        "id": post["id"],
        "title": post["title"],
        "content": post["content"],
        "author": post["author"],
        "password": post["password"],
        "graphData": post["graphData"],
        "comments": [Comment(**comment) for comment in post.get("comments", [])]
    }
    post2 = Post(**post_data)
    return post2


def update_post_from_db(post_id: int, post: Post):
    changing_post = db.posts.find_one({"id": post_id})

    if changing_post is None:
        return JSONResponse(status_code=404, content={"detail": "Post not found"})

    update_data = post.dict(exclude_unset=True)
    print(update_data)
    db.posts.update_one({"id": post_id}, {"$set": update_data})
    return JSONResponse(status_code=200, content={"message": "Post updated successfully."})


def delete_post_from_db(post_id: int, author: str, password: str):
    post = db.posts.find_one({"id": post_id})
    if post is None:
        return JSONResponse(status_code=404, content={"detail": "Post not found"})
    # 게시물의 작성자와 비밀번호가 요청과 일치하는지 확인
    if post.get("author") != author or post.get("password") != password:
        # 작성자 이름 또는 비밀번호가 일치하지 않는 경우, 오류 메시지 반환
        return JSONResponse(status_code=403, content={"detail": "Authorization failed"})

    db.posts.delete_one({"id": post_id})
    return JSONResponse(status_code=200, content={"message": "Post deleted successfully."})


def read_post_from_db(post_id: int):
    post = db.posts.find_one({"id": post_id})

    if post is None:
        return JSONResponse(status_code=404, content={"detail": "Post not found"})

    post2 = post_to_post2(post)

    return JSONResponse(status_code=200, content=post2.dict())


def get_post_from_db():
    posts = db.posts.find().sort("_id", -1)
    return posts


def create_post_from_db(post: Post):
    id_list = db.posts.find({}, sort=[("id", -1)]).limit(1)
    list_id = 0
    id_list = list(id_list)  # 커서를 리스트로 변환
    if id_list:
        list_id = incremental_id(id_list[0]["id"])
    post.id = list_id
    print(post)
    new_post = db.posts.insert_one(post.dict())

    if new_post.inserted_id:
        return {"message": "Post created successfully."}  # JSONResponse 대신 직접 반환
    else:
        return JSONResponse(content={"message": "Failed to create post."}, status_code=status.HTTP_400_BAD_REQUEST)

