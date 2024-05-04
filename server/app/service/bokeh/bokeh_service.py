# bokeh
from bokeh.models import (ColumnDataSource, DatetimeTickFormatter, HoverTool)
from bokeh.models.formatters import NumeralTickFormatter
from bokeh.palettes import Category10_10
from bokeh.plotting import figure

# data frame
import pandas as pd


def draw_dataframe_to_graph(df_list, facility_list):

    if len(df_list) == 1:
        return draw_single_dataframe_to_graph(df_list[0], facility_list[0])
    else:
        plots = []
        p = figure(title="Facility Comparison",sizing_mode="scale_both", x_axis_label='Time (seconds)',
                   y_axis_label='Value',
                   height=400)

        colors = Category10_10

        for i, df in enumerate(df_list):
            # 각 데이터프레임의 시작 시간을 추출하여 가장 빠른 시작 시간을 구합니다.
            # start_time = pd.to_datetime(df["Time"].str.replace("Z", ""), utc=True).min()
            start_time = pd.to_datetime(df["Time"], utc=True).min()

            # 데이터프레임의 이름을 가져옵니다.
            df_name = facility_list[i]

            # 시간 정보를 조정하여 모든 선이 같은 출발점에서 시작되도록 합니다.
            # df["Time"] = (pd.to_datetime(df["Time"].str.replace("Z", ""), utc=True) - start_time).dt.total_seconds()
            df["Time"] = (pd.to_datetime(df["Time"], utc=True) - start_time).dt.total_seconds()

            # 색상 선택
            color = colors[i % len(colors)]
            source = ColumnDataSource(data=df)


            for j, column_name in enumerate(df.columns[1:]):
                line = p.line(x='Time', y=column_name, source=source, legend_label=f"{df_name} - {column_name}",
                       color=color)

                hover = HoverTool(renderers=[line], tooltips=[
                    ('facility', f'{df_name}'),
                    ('time', '@Time seconds'),
                    ('Value', '$y')
                ])

                # max_value, min_value, average = calc_df_values(source, df_name, column_name)
                # average_line = Span(location=average, dimension='width', line_color=color, line_width=1)
                # p.add_layout(average_line)
                # average_hover = HoverTool(renderers=[line], tooltips=[
                #     ('facility', f'{df_name}'),
                #     ('Value', f'{average}')
                # ])
                # p.add_tools(average_hover)


            p.add_tools(hover)


            # # 최댓값과 최솟값 텍스트 추가
            # p.text(x=[0], y=[0], text=[f'Min: {min_value}, Max: {max_value}'], text_font_size="10pt",
            #        text_baseline="bottom", text_align="left", text_color="black")

        p.x_range.start = 0
        p.xaxis.formatter = NumeralTickFormatter(format="0")
        p.legend.location = "top_left"
        plots.append(p)

        return plots


def draw_single_dataframe_to_graph(df, facility):

    plots = []
    all_data = []

    # "Z" 제거
    # df["Time"] = df["Time"].str.replace("Z", "")

    # pd.to_datetime을 사용하여 변환
    time_values = pd.to_datetime(df["Time"], utc=True)

    combined_data = dict(x=time_values)
    for column in df.columns:
        if column != "Time":
            column_data = df[column]
            all_data.append(column_data)
            combined_data[column] = column_data.values

    source = ColumnDataSource(data=combined_data)

    p = figure(title="facility", sizing_mode="scale_both", x_axis_label='Time', y_axis_label='Value',
               height=800)

    for i, column_name in enumerate(df.columns[1:]):
        line = p.line(x='x', y=column_name, source=source, legend_label=column_name, color=Category10_10[i])

        hover = HoverTool(renderers=[line], tooltips=[
            ('facility', f'{facility}'),
            ('time', '@x{%H:%M:%S}'),
            ('Value', '$y')
        ],  formatters={'@x': 'datetime'})

    p.add_tools(hover)

    p.xaxis.formatter = DatetimeTickFormatter(hours='%H:%M:%S')
    p.legend.location = "top_left"
    plots.append(p)

    return plots


# ColumnDataSource의 max, min, 평균 값 구하기
def calc_df_values(source, df_name,column_name):
    print("========== source 테스트 ===========")
    print(f'source : {source} facility : {df_name} column : {column_name}')
    max_value = max(source.data[column_name])
    min_value = min(source.data[column_name])
    average = source.data[column_name].mean()
    print(f'{df_name} 의 최댓값 {max_value}')
    print(f'{df_name} 의 최솟값 {min_value}')
    print(f'{df_name} 의 평균값 {average}')
    print("===================================")
    return max_value, min_value, average



