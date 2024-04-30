# fastapi
import uvicorn
from fastapi import FastAPI, HTTPException, File, UploadFile
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


file_name = "F1492-ExhaustLog-240323-011325.CSV"

column = "No6_P1_Fwd[kW]"
columns = ["No1_P[kW]","No2_P[kW]","No4_P[kW]","No5_P[kW]"
           ,"No6_P1_Fwd[kW]","No6_P2_Fwd[kW]","No6_P3_Fwd[kW]", "No6_P4_Fwd[kW]"
           ,"No6_A1[sccm]", "No6_O1[sccm]","No6_O2[sccm]","No6_N1[sccm]"
           ,"No1_A1[sccm]","No1_A2[sccm]","No1_A3[sccm]","No1_A4[sccm]"
           ,"No2_A1[sccm]","No2_A2[sccm]","No2_A3[sccm]","No2_A4[sccm]"
           ,"No4_A1[sccm]","No4_A2[sccm]","No4_A3[sccm]","No4_A4[sccm]"
           ,"No5_A1[sccm]","No5_A2[sccm]","No5_A3[sccm]","No5_A4[sccm]"]

tg_file_name = "F1508-ExhaustLog-240412-012855.CSV"
tg_columns = ["P.TG1Pwr[kW]","P.MF211Ar[sccm]","P.MF212Ar[sccm]","P.MF213Ar[sccm]","P.MF214Ar[sccm]"
                  ,"P.TG2Pwr[kW]","P.MF221Ar[sccm]","P.MF222Ar[sccm]","P.MF223Ar[sccm]","P.MF224Ar[sccm]"
                  ,"P.TG4Pwr[kW]","P.MF241Ar[sccm]","P.MF242Ar[sccm]","P.MF243Ar[sccm]","P.MF244Ar[sccm]"
                  ,"P.TG5Pwr[kW]","P.MF251Ar[sccm]","P.MF252Ar[sccm]","P.MF253Ar[sccm]","P.MF254Ar[sccm]"
                  ,"P.Icp1PwrFwd[kW]","P.Icp2PwrFwd[kW]","P.Icp3PwrFwd[kW]","P.Icp4PwrFwd[kW]"
                  ,"P.MF207Ar[sccm]","P.MF208O2[sccm]","P.MF209O2[sccm]","P.MF210N2[sccm]"]

start = 1120
end = 4948

tg_start = 1026
tg_end = 5687

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
    print(df)

# 파일 업로드 하는 함수
def load_file(file_name):
    try:
        df = pd.read_csv(file_name)
        print(df)
        return df
    except Exception as e:
        print("파일 불러오기 실패", e)
        return None

# df = load_file(file_name)
# tg 파일 읽기
df = load_file(tg_file_name)
print(type(df))
print(df)
#
#
# # 출력을 노트북에 표시
# output_notebook()

# 특정 구간 그래프 그리는 함수
def draw_graph(column, start, end):
    column_data = df[str(column)].iloc[start:end]
    data_length = len(column_data)

    # Bokeh에서는 ColumnDataSource를 사용하여 데이터를 전달
    source = ColumnDataSource(data=dict(x=np.linspace(start, end, data_length), y=column_data))

    # figure 객체 생성
    p = figure(title='Line Plot of Data in {} Column'.format(str(column)),
               x_axis_label='Index', y_axis_label='Value')

    # 선 그래프 추가
    p.line(x='x', y='y', source=source, legend_label="Line Plot of Data in {} Column".format(column))

    # 범례 표시
    p.legend.location = "top_left"

    return p

# 전체 그래프 그리는 함수
def draw_all_graph(columns, start, end):
    plots = []
    for i in range(len(columns)):
        column = df[str(columns[i])].iloc[start:end]
        print("============column=============")
        print(column)
        print("==========type============")
        print(type(column))
        data_length = len(column)

        # Bokeh에서는 ColumnDataSource를 사용하여 데이터를 전달
        source = ColumnDataSource(data=dict(x=np.linspace(start, end, data_length), y=column))
        # source = ColumnDataSource(data=dict(x=np.linspace(start, end, data_length).astype(str), y=column))
        print("==========1번 source============")
        print(source.data)
        print("=========1번 source 타입===============")
        print(type(source.data))
        x = np.linspace(start, end, data_length)
        print(type(x[0]))
        # figure 객체 생성
        p = figure(title='Line Plot of Data in {} Column'.format(str(columns[i])),
                   x_axis_label='Index', y_axis_label='Value')

        # 선 그래프 추가
        p.line(x='x', y='y', source=source, legend_label="Line Plot of Data in {} Column".format(columns[i]))

        # 범례 표시
        p.legend.location = "top_left"

        plots.append(p)
    return plots

# 전체 그래프 그리는 함수
def draw_all_graph_2(columns, start, end):
    plots = []
    for i in range(len(columns)):
        column = df[str(columns[i])].iloc[start:end]
        time_values = df["Time"].iloc[start:end].values
        time_values = pd.to_datetime(time_values)
        print(time_values)

        # 원하는 시간 형식으로 포맷팅
        # time_values_formatted = time_values.strftime("%H:%M:%S")
        data_length = len(column)

        # Bokeh에서는 ColumnDataSource를 사용하여 데이터를 전달
        source = ColumnDataSource(data=dict(x=time_values, y=column))

        # figure 객체 생성
        p = figure(title='Line Plot of Data in {} Column'.format(str(columns[i])),
                   x_axis_label='Time', y_axis_label='Value')

        # 선 그래프 추가
        p.line(x='x', y='y', source=source, legend_label="Line Plot of Data in {} Column".format(columns[i]))

        # x 축의 레이블 포맷 지정
        p.xaxis.formatter = DatetimeTickFormatter(hours='%H:%M:%S')

        # 범례 표시
        p.legend.location = "top_left"

        plots.append(p)
    return plots


def draw_all_tg_graph(df, tg_start, tg_end):
    plots = []
    columns = df.columns.tolist()  # 데이터프레임의 모든 열 이름 가져오기
    print("================columns================")
    print(columns)
    time_values = pd.to_datetime(df["Time"].iloc[tg_start:tg_end].values)

    for column in columns:
        if column != "Time":  # Time 열은 이미 가져왔으므로 건너뜁니다.
            tg_column = df[column].iloc[tg_start:tg_end]

            # Bokeh에서는 ColumnDataSource를 사용하여 데이터를 전달합니다.
            source = ColumnDataSource(data=dict(x=time_values, y=tg_column))

            # figure 객체 생성
            p = figure(title='Line Plot of Data in {} Column'.format(column),
                       x_axis_label='Time', y_axis_label='Value')

            # 선 그래프 추가
            p.line(x='x', y='y', source=source, legend_label="Line Plot of Data in {} Column".format(column))

            # x 축의 레이블 포맷 지정
            p.xaxis.formatter = DatetimeTickFormatter(hours='%H:%M:%S')

            # 범례 표시
            p.legend.location = "top_left"

            plots.append(p)
    return plots

# 예시로 사용할 데이터프레임 생성
# df = pd.read_csv("your_csv_file.csv")  # CSV 파일을 불러와서 데이터프레임 생성
# tg_start, tg_end = 0, len(df)  # 데이터프레임의 전체 범위를 사용하려면 이렇게 지정하세요.

# 그래프 생성
# plots = draw_all_tg_graph(df, tg_start, tg_end)
# for plot in plots:
#     show(plot)  # 그래프 출력


# import pandas as pd
# from bokeh.plotting import figure
# from bokeh.models import ColumnDataSource, DatetimeTickFormatter
#
# def draw_all_tg_graph(df, tg_start, tg_end):
#     plots = []
#     if "Time" in df.columns:
#         time_values = pd.to_datetime(df["Time"].iloc[tg_start:tg_end].values)
#     else:
#         raise ValueError("Time column not found in the DataFrame.")
#
#     for column in df.columns:
#         if column != "Time":
#             tg_column = df[column].iloc[tg_start:tg_end]
#
#             source = ColumnDataSource(data=dict(x=time_values, y=tg_column))
#
#             p = figure(title='Line Plot of Data in {} Column'.format(column),
#                        x_axis_label='Time', y_axis_label='Value')
#
#             p.line(x='x', y='y', source=source, legend_label="Line Plot of Data in {} Column".format(column))
#
#             p.xaxis.formatter = DatetimeTickFormatter(hours='%H:%M:%S')
#
#             p.legend.location = "top_left"
#
#             plots.append(p)
#     return plots

# 예시로 사용할 데이터프레임 생성
# df = pd.read_csv("your_csv_file.csv")  # CSV 파일을 불러와서 데이터프레임 생성
# tg_start, tg_end = 0, len(df)  # 데이터프레임의 전체 범위를 사용하려면 이렇게 지정하세요.

# 그래프 생성
# plots = draw_all_tg_graph(df, tg_start, tg_end)
# for plot in plots:
#     show(plot)  # 그래프 출력


@app.get("/draw_graph")
async def draw_graph_endpoint():
    plot = draw_graph(columns, start, end)
    plot_json = json_item(plot, "my_plot")
    return JSONResponse(content=plot_json)


@app.get("/draw_all_graph")
async def draw_graph_endpoint():
    plots = draw_all_graph(columns, start, end)
    plot_json = [json_item(plot, f"my_plot_{idx}") for idx, plot in enumerate(plots)]
    return JSONResponse(content=plot_json)

@app.get("/draw_all_graph_2")
async def draw_graph_endpoint():
    plots = draw_all_graph_2(columns, start, end)
    plot_json = [json_item(plot, f"my_plot_{idx}") for idx, plot in enumerate(plots)]
    return JSONResponse(content=plot_json)

# @app.get("/draw_all_tg_graph")
# async def draw_graph_endpoint():
#     plots = draw_all_tg_graph(tg_columns, tg_start, tg_end)
#     plot_json = [json_item(plot, f"my_plot_{idx}") for idx, plot in enumerate(plots)]
#     return JSONResponse(content=plot_json)

@app.get("/draw_all_tg_graph")
async def draw_graph_endpoint():
    plots = draw_all_tg_graph(df, tg_start, tg_end)
    plot_json = [json_item(plot, f"my_plot_{idx}") for idx, plot in enumerate(plots)]
    return JSONResponse(content=plot_json)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)