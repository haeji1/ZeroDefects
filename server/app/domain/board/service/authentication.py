from pymongo import MongoClient

from config import settings

url = settings.mongo_furl

# MongoDB client
client = MongoClient(url)
# database name is setting
db = client["post"]


# def authenticate_user(nickname: str, password: str):
#     if nickname in fake_user_db and fake_user_db[nickname]["password"] == password:
#         return True
#     return False