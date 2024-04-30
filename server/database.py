# 필요한 라이브러리 import하기
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

# SQLAlchemy 사용할 DB URL 생성하기
SQLALCHEMY_DATABASE_URL = "postgresql://ssafy:ssafy@localhost:5432/s107"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@host:port/db"

# SQLAlchemy engine 생성하기
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# DB 세션 생성하기
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class 생성하기
Base = declarative_base()