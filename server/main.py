# fastapi
import uvicorn
from fastapi import FastAPI, HTTPException, File, UploadFile
from app.routers.bokehgraph import bokeh_router
from fastapi.responses import JSONResponse

# bokeh
from bokeh.models import ColumnDataSource, DatetimeTickFormatter
from bokeh.plotting import figure
from bokeh.embed import json_item

# postgreSQL
from database import engine
from psycopg2 import IntegrityError
from datetime import datetime, timedelta

# data frame
import pandas as pd
import numpy as np

# cors
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "*",
]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # cross-origin request에서 cookie를 포함할 것인지 (default=False)
    allow_methods=["*"],     # cross-origin request에서 허용할 method들을 나타냄. (default=['GET']
    allow_headers=["*"],     # cross-origin request에서 허용할 HTTP Header 목록
)

app.include_router(bokeh_router.router)
@app.post("/upload/csv")
async def upload_csv(file: UploadFile = File(...)):

    table_name = file.filename.split('-')[0]
    date_info = file.filename.split('-')[2]

    df = pd.read_csv(file.file)

    # df의 컬럼 데이터 타입 확인
    print(df.dtypes)

    # 'time' 컬럼에 날짜 추가하기
    if 'Time' in df.columns:
        df['Time'] = pd.to_datetime(df['Time']).apply(
            lambda x: x.replace(year=int("20" + date_info[:2]), month=int(date_info[2:4]), day=int(date_info[4:6])))

    flag = False
    for index, row in df.iterrows():
        if row['Time'].time() == datetime.strptime("00:00:00", "%H:%M:%S").time():
            flag = True
        if flag:
            df.at[index, 'Time'] = row['Time'] + timedelta(days=1)

    try:
        df.to_sql(table_name, engine, index=False, if_exists='append')

        # 중복된 'Time' 값을 가진 로우 제거
        engine.execute(f"""
        DELETE FROM {table_name}
        WHERE rowid NOT IN (
            SELECT MIN(rowid)
            FROM {table_name}
            GROUP BY Time
        )
        """)
    except IntegrityError as e:
        print(e)

@app.get("/items/{facility}")
async def get_facility(facility):

    # SQL 쿼리를 사용하여 데이터베이스에서 데이터 읽기
    query = 'SELECT * FROM public."{}"'.format(facility)

    # 데이터를 pandas DataFrame으로 읽기
    df = pd.read_sql_query(query, engine)
    print(df)

    return {"records": df.to_dict('records')}

# 수정해서 사용하세요.
async def read_facility(facility):
    # SQL 쿼리를 사용하여 데이터베이스에서 데이터 읽기
    query = 'SELECT * FROM public."{}"'.format(facility)

    # 데이터를 pandas DataFrame으로 읽기
    df = pd.read_sql_query(query, engine)
    # print(df)

# 파일 업로드 하는 함수



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)