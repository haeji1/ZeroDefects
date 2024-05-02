# bokeh
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, BasicTickFormatter
from bokeh.palettes import Category10_10
from bokeh.plotting import figure


# data frame
import pandas as pd


def draw_dataframe_to_graph(df_list):
    if len(df_list) == 1:  # 데이터프레임이 하나일 때
        return draw_single_dataframe_to_graph(df_list[0])
    else:  # 데이터프레임이 여러 개일 때
        plots = []

        # 각 데이터프레임의 시작 시간을 추출하여 가장 빠른 시작 시간을 구합니다.
        start_times = [pd.to_datetime(df["Time"].str.replace("Z", ""), utc=True).min() for df in df_list]
        min_start_time = min(start_times)

        # 각 데이터프레임의 시간 정보를 조정하여 모든 선이 같은 출발점에서 시작되도록 합니다.
        for df, start_time in zip(df_list, start_times):
            df["Time"] = (pd.to_datetime(df["Time"].str.replace("Z", ""), utc=True) - start_time).dt.total_seconds()

        # 모든 데이터프레임을 하나의 데이터프레임으로 합칩니다.
        combined_df = pd.concat(df_list, ignore_index=True)

        # ColumnDataSource 생성
        source = ColumnDataSource(data=combined_df)

        # figure 객체 생성
        p = figure(title="facility", x_axis_label='Time (seconds)', y_axis_label='Value',
                   width=1200, height=400)

        # 각 컬럼 데이터를 그래프에 추가하면서 다른 색상 지정
        for i, column_name in enumerate(combined_df.columns[1:]):  # 첫 번째 컬럼은 'Time'이므로 제외합니다
            p.line(x='Time', y=column_name, source=source, legend_label=column_name, color=Category10_10[i])

        # 범례 표시
        p.legend.location = "top_left"

        plots.append(p)

        return plots

def draw_single_dataframe_to_graph(df):
    plots = []

    # 전체 데이터를 담을 빈 리스트 생성
    all_data = []

    # "Z" 제거
    df["Time"] = df["Time"].str.replace("Z", "")

    # pd.to_datetime을 사용하여 변환
    time_values = pd.to_datetime(df["Time"], utc=True)

    # 각 컬럼 데이터를 하나의 ColumnDataSource로 결합
    combined_data = dict(x=time_values)

    for column in df.columns:
        if column != "Time":
            column_data = df[column]
            all_data.append(column_data)
            combined_data[column] = column_data.values

    # ColumnDataSource 생성
    source = ColumnDataSource(data=combined_data)

    # figure 객체 생성
    p = figure(title="facility", x_axis_label='Time', y_axis_label='Value',
               width=1200, height=400)

    # 각 컬럼 데이터를 그래프에 추가하면서 다른 색상 지정
    for i, column_name in enumerate(df.columns[1:]):  # 첫 번째 컬럼은 'Time'이므로 제외합니다
        p.line(x='x', y=column_name, source=source, legend_label=column_name, color=Category10_10[i])

    p.xaxis.formatter = DatetimeTickFormatter(hours='%H:%M:%S')
    # 범례 표시
    p.legend.location = "top_left"

    plots.append(p)

    return plots