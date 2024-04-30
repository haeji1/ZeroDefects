
file_name = "F1492-ExhaustLog-240323-011325.CSV"

column = "No1_P[kW]"
columns = ["No1_P[kW]","No2_P[kW]","No4_P[kW]","No5_P[kW]"
    ,"No6_P1_Fwd[kW]","No6_P2_Fwd[kW]","No6_P3_Fwd[kW]", "No6_P4_Fwd[kW]"
    ,"No6_A1[sccm]", "No6_O1[sccm]","No6_O2[sccm]","No6_N1[sccm]"
    ,"No1_A1[sccm]","No1_A2[sccm]","No1_A3[sccm]","No1_A4[sccm]"
    ,"No2_A1[sccm]","No2_A2[sccm]","No2_A3[sccm]","No2_A4[sccm]"
    ,"No4_A1[sccm]","No4_A2[sccm]","No4_A3[sccm]","No4_A4[sccm]"
    ,"No5_A1[sccm]","No5_A2[sccm]","No5_A3[sccm]","No5_A4[sccm]"]

start = 1120
end = 4948

# bokeh
from bokeh.models import ColumnDataSource, DatetimeTickFormatter
from bokeh.palettes import Category10_10
from datetime import date, time
from bokeh.plotting import figure
from pydantic import BaseModel
from typing import List


# data frame
import pandas as pd
import numpy as np

def load_file(file_name):
    try:
        df = pd.read_csv(file_name)
        print(df)
        return df
    except Exception as e:
        print("파일 불러오기 실패", e)
        return None


file_name = "F1492-ExhaustLog-240323-011325.CSV"
df = load_file(file_name)

# 특정 그래프 그리는 함수
def draw_graph(column, start, end):
    print("===============column=============")
    print(column)
    column_data = df[str(column)].iloc[start:end]
    data_length = len(column_data)

    print('===============baboyuncheolbabo===============', column_data)

    # Bokeh에서는 ColumnDataSource를 사용하여 데이터를 전달
    source = ColumnDataSource(data=dict(x=np.linspace(start, end, data_length), y=column_data))

    # figure 객체 생성
    p = figure(title='Line Plot of Data in {} Column'.format(str(column)),
               x_axis_label='Index', y_axis_label='Value')
    print("=================p=================")
    print(p)
    # 선 그래프 추가
    p.line(x='x', y='y', source=source, legend_label="Line Plot of Data in {} Column".format(column))

    # 범례 표시
    p.legend.location = "top_left"

    return p

draw_graph(column, start, end)
# 전체 그래프 그리는 함수
def draw_all_graph(columns, start, end):
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


def get_bokeh_data(graph_data):

    data = {
        "start_time": [],
        "end_time": [],
        "facilities": [],
        "parameters": []
    }

    for item in graph_data:
        data["start_time"].append(item.startDate + " " + item.startTime)
        data["end_time"].append(item.endDate + " " + item.endTime)
        data["facilities"].append(item.facility)
        data["parameters"].append(item.parameter)

    return data

