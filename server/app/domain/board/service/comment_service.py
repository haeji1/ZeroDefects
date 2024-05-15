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


def create_comment_from_db(post_id: int, comment: Comment):
    # 특정 게시물 찾기
    post = db.posts.find_one({"id": post_id})
    if post is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Post not found"})

    # 댓글 목록에 새 댓글 추가
    if "comments" not in post:
        post["comments"] = []
    comment.id = len(post["comments"])
    post["comments"].append(comment.dict())

    # 게시물 업데이트
    db.posts.update_one({"id": post_id}, {"$set": {"comments": post["comments"]}})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Comment added successfully."})


def get_comments_from_db(post_id: int):
    post = db.posts.find_one({"id": post_id})
    if post is None or "comments" not in post:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "No comments found"})

    comments = post["comments"]
    return JSONResponse(status_code=status.HTTP_200_OK, content={"comments": comments})


def update_comment_in_db(post_id: int, comment_id: int, updated_comment: Comment):
    # 특정 게시물 찾기
    post = db.posts.find_one({"id": post_id})
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    # 댓글 목록에서 해당 댓글 찾기
    comments = post.get("comments", [])
    comments[comment_id] = updated_comment.dict(exclude_unset=True)

    # 게시물 업데이트
    db.posts.update_one({"id": post_id}, {"$set": {"comments": comments}})

    return {"message": "Comment updated successfully."}


def delete_comment_from_db(post_id: int, comment_id: int, author: str, password: str):
    # 특정 게시물 찾기
    post = db.posts.find_one({"id": post_id})
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    # 댓글 목록에서 해당 댓글 찾아 삭제
    original_comments = post.get("comments", [])
    new_comments = [comment for comment in original_comments if comment["id"] != comment_id]
    comment = original_comments[comment_id]
    print(comment)
    # 게시물의 작성자와 비밀번호가 요청과 일치하는지 확인
    if comment.get("author") != author or comment.get("password") != password:
        # 작성자 이름 또는 비밀번호가 일치하지 않는 경우, 오류 메시지 반환
        return JSONResponse(status_code=403, content={"detail": "Authorization failed"})

    if len(original_comments) == len(new_comments):
        raise HTTPException(status_code=404, detail="Comment not found")

    # 게시물 업데이트
    db.posts.update_one({"id": post_id}, {"$set": {"comments": new_comments}})

    return {"message": "Comment deleted successfully."}
