# import os
#
# from fastapi import Depends, HTTPException
# from fastapi.security import HTTPBasic, HTTPBasicCredentials
# from pymongo import MongoClient
# from passlib.context import CryptContext
#
# from app.domain.board.model.board import Post
#
# url = os.getenv('MONGO_FURL')
# client = MongoClient(url)
# db = client["board"]
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# security = HTTPBasic()
#
#
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)
#
#
# def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
#     user = db.posts.find_one({"author": credentials.username})
#     if user and verify_password(credentials.password, user['password']):
#         return credentials.username
#     raise HTTPException(status_code=400, detail="Incorrect email or password")
#
#
# async def create_post(post: Post):
#     post_dict = post.dict()
#     post_dict['password'] = pwd_context.hash(post_dict['password'])
#     db.posts.insert_one(post_dict)
#     return {"message": "Post created successfully"}

def incremental_id(id):
    return id + 1