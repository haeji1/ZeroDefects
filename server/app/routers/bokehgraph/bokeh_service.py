# bokeh
from bokeh.models import ColumnDataSource, DatetimeTickFormatter
from bokeh.palettes import Category10_10
from bokeh.plotting import figure


# data frame
import pandas as pd
import numpy as np


# def load_file(file_name):
#     try:
#         df = pd.read_csv(file_name)
#         # print(df)
#         return df
#     except Exception as e:
#         print("파일 불러오기 실패", e)
#         return None
#
# file_name = "F1492-ExhaustLog-240323-011325.CSV"
# df = load_file(file_name)
# print(df)
# print("==============컬럼이름===============")
# print(df.columns)
#
# # 특정 그래프 그리는 함수
# def draw_graph(column, start, end):
#     print("===============column=============")
#     print(column)
#     column_data = df[str(column)].iloc[start:end]
#     data_length = len(column_data)
#
#     print('===============baboyuncheolbabo===============', column_data)
#     print("----------------------------------", column_data.size)
#
#     # Bokeh에서는 ColumnDataSource를 사용하여 데이터를 전달
#     source = ColumnDataSource(data=dict(x=np.linspace(start, end, data_length), y=column_data))
#
#     # figure 객체 생성
#     p = figure(title='Line Plot of Data in {} Column'.format(str(column)),
#                x_axis_label='Index', y_axis_label='Value')
#     print("=================p=================")
#     print(p)
#     # 선 그래프 추가
#     p.line(x='x', y='y', source=source, legend_label="Line Plot of Data in {} Column".format(column))
#
#     # 범례 표시
#     p.legend.location = "top_left"
#
#     return p
#
# draw_graph(column, start, end)
# # 전체 그래프 그리는 함수
# def draw_all_graph(columns, start, end):
#     plots = []
#     for i in range(len(columns)):
#         column = df[str(columns[i])].iloc[start:end]
#         time_values = df["Time"].iloc[start:end].values
#         time_values = pd.to_datetime(time_values)
#         print(time_values)
#
#         # 원하는 시간 형식으로 포맷팅
#         # time_values_formatted = time_values.strftime("%H:%M:%S")
#         data_length = len(column)
#
#         # Bokeh에서는 ColumnDataSource를 사용하여 데이터를 전달
#         source = ColumnDataSource(data=dict(x=time_values, y=column))
#
#         # figure 객체 생성
#         p = figure(title='Line Plot of Data in {} Column'.format(str(columns[i])),
#                    x_axis_label='Time', y_axis_label='Value')
#
#         # 선 그래프 추가
#         p.line(x='x', y='y', source=source, legend_label="Line Plot of Data in {} Column".format(columns[i]))
#
#         # x 축의 레이블 포맷 지정
#         p.xaxis.formatter = DatetimeTickFormatter(hours='%H:%M:%S')
#
#         # 범례 표시
#         p.legend.location = "top_left"
#
#         plots.append(p)
#     return plots
#
#
# def draw_all_tg_graph(df, tg_start, tg_end):
#     plots = []
#     columns = df.columns.tolist()  # 데이터프레임의 모든 열 이름 가져오기
#     print("================columns================")
#     print(columns)
#     time_values = pd.to_datetime(df["Time"].iloc[tg_start:tg_end].values)
#
#     for column in columns:
#         if column != "Time":  # Time 열은 이미 가져왔으므로 건너뜁니다.
#             tg_column = df[column].iloc[tg_start:tg_end]
#
#             # Bokeh에서는 ColumnDataSource를 사용하여 데이터를 전달합니다.
#             source = ColumnDataSource(data=dict(x=time_values, y=tg_column))
#
#             # figure 객체 생성
#             p = figure(title='Line Plot of Data in {} Column'.format(column),
#                        x_axis_label='Time', y_axis_label='Value')
#
#             # 선 그래프 추가
#             p.line(x='x', y='y', source=source, legend_label="Line Plot of Data in {} Column".format(column))
#
#             # x 축의 레이블 포맷 지정
#             p.xaxis.formatter = DatetimeTickFormatter(hours='%H:%M:%S')
#
#             # 범례 표시
#             p.legend.location = "top_left"
#
#             plots.append(p)
#     return plots
#
# # 가져온 DataFrame을 가지고 그래프 그리는 함수
# # def draw_dataframe_to_graph(df_list):
# #     plots = []
# #
# #     # 컬럼 이름 모두 알아내기
# #     for df in df_list:
# #         columns = df.columns.tolist()
# #         time_values = pd.to_datetime(df["Time"])
# #
# #         for column in columns:
# #             if column != "Time":
# #                 column_values = df[column].values
# #                 source = ColumnDataSource(data=dict(x=time_values, y=column_values))
# #
# #                 # figure 객체 생성
# #                 p = figure(title='Line Plot of Data in {} Column'.format(column),x_axis_label='Time', y_axis_label=column,
# #                            plot_width=None, plot_height=400)
# #
# #                 # 선 그래프 추가
# #                 p.line(x='x', y='y', source=source, legend_label="Line Plot of Data in {} Column".format(column))
# #                 # x 축의 레이블 포맷 지정
# #                 p.xaxis.formatter = DatetimeTickFormatter(hours='%H:%M:%S')
# #
# #                 # 범례 표시
# #                 p.legend.location = "top_left"
# #
# #                 plots.append(p)
# #     return plots
#
#
def draw_dataframe_to_graph(df_list, facility_list):
    plots = []

    # 전체 데이터를 담을 빈 리스트 생성
    all_data = []

    print("========facility 출력========")
    for facility in facility_list:
        print(facility)
        print("======길이=======")
        print(len(facility_list))
        print("======facility=====")
        print(facility_list)

        # 컬럼 이름 모두 알아내기
        for df in df_list:
            columns = df.columns.tolist()
            # print("------------columns-----------")
            # print(columns)
            # print("==========dfTime==============")
            # print(df["Time"])
            # print(type(df["Time"].iloc[0]))
            # print("=====dfTimetype=======")
            # print(type(df["Time"]))

            # "Z" 제거
            df["Time"] = df["Time"].str.replace("Z", "")

            # pd.to_datetime을 사용하여 변환
            time_values = pd.to_datetime(df["Time"], utc=True)
            # print("===============")
            # print("==========Z 제거하고 dattime으로 변환==============")
            # print(time_values)

            # 각 컬럼 데이터를 하나의 ColumnDataSource로 결합
            combined_data = dict(x=time_values)

            for column in columns:
                if column != "Time":
                    column_data = df[column]
                    all_data.append(column_data)
                    combined_data[column] = column_data.values

            # ColumnDataSource 생성
            source = ColumnDataSource(data=combined_data)

            # figure 객체 생성
            p = figure(title=facility, x_axis_label='Time', y_axis_label='Value',
                       width=1200, height=400)

            # 각 컬럼 데이터를 그래프에 추가하면서 다른 색상 지정
            for i, column_name in enumerate(columns[1:]):  # 첫 번째 컬럼은 'Time'이므로 제외합니다
                p.line(x='x', y=column_name, source=source, legend_label=column_name, color=Category10_10[i])

            p.xaxis.formatter = DatetimeTickFormatter(hours='%H:%M:%S')
            # 범례 표시
            p.legend.location = "top_left"
            print("=========legend============")
            print(p.legend)

            plots.append(p)

        return plots
