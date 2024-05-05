# from datetime import time
#
# import pandas as pd
# from fastapi import APIRouter, File, UploadFile, HTTPException
#
# import psycopg2
# from psycopg2.extras import execute_values
#
# from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, String, DateTime
# from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
# from sqlalchemy.orm import sessionmaker
#
# from starlette.responses import JSONResponse
#
# import time
#
# # SQLAlchemy 엔진 생성
# engine = create_engine('postgresql://postgres:12341234@localhost:5432/postgres')
#
# # 세션 생성
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# connection = engine.connect()
# metadata = MetaData()
#
# def connect_db():
#     conn = psycopg2.connect(
#         host="localhost",
#         port=5432,
#         database="postgres",
#         user="postgres",
#         password="12341234"
#     )
#     return conn
#
# table_name = 'TEST2'
#
# timescale_router = APIRouter(prefix="/timescale", tags=['/test'])
#
# @timescale_router.post("/write")
# async def write_data(file: UploadFile = File(...)):
#     start_time = time.time()
#     if file.content_type != 'text/csv':
#         return JSONResponse(status_code=400, content={"message": "Invalid file type"})
#
#     # file to df
#     df = pd.read_csv(file.file)
#
#     columns = []
#     for col_name in df.columns:
#         col_type = df[col_name].dtype
#         if col_type == 'int64':
#             col_type = Integer()
#         elif col_type == 'float64':
#             col_type = DOUBLE_PRECISION
#         elif col_type == 'datetime64[ns]':
#             col_type = DateTime()
#         else:
#             col_type = String()
#
#         column = Column(col_name, col_type)
#         columns.append(column)
#
#     table = Table(table_name, metadata, *columns)
#     metadata.create_all(engine)  # 테이블 생성
#
#     df.to_sql(table_name, con=engine, index=False, if_exists='replace')
#     print('total time: ', time.time() - start_time)
#
#     return JSONResponse(status_code=200, content={"message": time.time() - start_time})
#     #
#     # # to float
#     # # float_cols = df.columns.drop('Time')
#     # # df[float_cols] = df[float_cols].astype(float)
#     #
#     # # 'Time' -> datetime
#     # df['Time'] = pd.to_datetime('2024-05-05 ' + df['Time'], format='%Y-%m-%d %H:%M:%S')
#     #
#     # df.to_sql('TEST', con=engine, if_exists='replace', index=False)
#     # return JSONResponse(status_code=200, content={"message": "Data written successfully"})
#     # try:
#     #     # connect database
#     #     conn = connect_db()
#     #     cursor = conn.cursor()
#     #
#     #     # columns
#     #     columns = ', '.join([f'"{col}"' for col in df.columns])
#     #     placeholders = ','.join(['%s'] * len(df.columns))
#     #
#     #
#     #     for _, row in df.iterrows():
#     #         tuple(row)
#     #         sql = f"INSERT INTO TEST ({columns}) VALUES ({placeholders})"
#     #         cursor.execute(sql)
#     #         execute_values(cursor, )
#     #
#     #     conn.commit()
#     #     cursor.close()
#     #     conn.close()
#     #
#     #     return JSONResponse(status_code=200, content={"message": "Data written successfully"})
#     # except Exception as e:
#     #     print('error : ', str(e))
#     #     return  HTTPException(status_code=500, detail=str(e))
#
# @timescale_router.get("/read")
# async def read_data():
#     start_time = time.time()
#
#     # 시간, 설비, 인자
#     query = (f'SELECT * FROM "{table_name}" WHERE "date" BETWEEN \'1970-00-00 00:00:00+05:30\' AND \'2024-05-05 00:00:00+05:30\'')
#     df = pd.read_sql(query, connect_db())
#     print(df)
#
#     print('total time: ', time.time() - start_time)
#     return JSONResponse(status_code=200, content={"message": time.time() - start_time})