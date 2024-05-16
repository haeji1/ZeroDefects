# bokeh
from bokeh.layouts import column, row
from bokeh.models import ( TableColumn, DataTable, Toggle,CrosshairTool)

from bokeh.models import (DatetimeTickFormatter, HoverTool, ColumnDataSource, Range1d, BoxAnnotation)
from bokeh.models.formatters import NumeralTickFormatter
from bokeh.models import Span
from bokeh.palettes import Category10_10
from bokeh.plotting import figure

# data frame
import pandas as pd

def draw_dataframe_to_graph(graph_type, graph_df, steps_times_info=None, batch_name_list=None):
    # save_graph_data(graph_df)
    # extract_axis_info(graph_df)
    if graph_type == "time":
        return draw_graph_time_standard(graph_df)
    elif graph_type == "step":
        return draw_graph_step_standard(graph_df, steps_times_info, batch_name_list)


def draw_graph_time_standard(graph_df):
    # print("graph_df =", graph_df)
    if (len(graph_df) == 0):
        return []

    colors = Category10_10

    plots = []
    p = figure(title="Facility Comparison", sizing_mode="scale_width", x_axis_label='Time',
               y_axis_label='Value', max_height=1000)

    for df in graph_df:
        time_values = pd.to_datetime(df['Time'], utc=True)
        df["Time"] = pd.to_datetime(df["Time"])

        facility, column_name = df.columns[-1].split('-')

        color = colors[len(p.renderers) % len(colors)]
        source = ColumnDataSource(data={'Time': time_values, 'Value': df[df.columns[-1]]})
        line = p.line(x='Time', y='Value', source=source, legend_label=f'{facility} - {column_name}', color=color)
        hover = HoverTool(renderers=[line], tooltips=[
                     ('facility', f'{facility}'),
                     ('time', '@Time{%F %T}'),
                     ('Value', '$y')
                 ], formatters={'@Time': 'datetime'})

        p.add_tools(hover)

        # CrosshairTool 생성
        width = Span(dimension="width", line_dash="dotted", line_width=1)
        height = Span(dimension="height", line_dash="dotted", line_width=1)
        p.add_tools(CrosshairTool(overlay=[width, height]))

    # DataTable 생성
    combined_df = pd.concat(graph_df)
    source = ColumnDataSource(combined_df)

    columns = [
        TableColumn(field=c, title=c) for c in combined_df.columns
    ]

    data_table = DataTable(source=source, columns=columns, editable=True, index_position=0, index_header="row",
                           sizing_mode="stretch_width")

    all_time_values = pd.concat([df['Time'] for df in graph_df])
    min_time = all_time_values.min()
    max_time = all_time_values.max()

    p.x_range = Range1d(min_time, max_time)

    p.xaxis.formatter = DatetimeTickFormatter(hours='%H:%M:%S')
    p.yaxis.formatter = NumeralTickFormatter(format="0,0")
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    p.toolbar.autohide = True
    p.toolbar.logo = None

    # 그래프와 데이터 테이블을 수직으로 배치
    layout = column([p, data_table], sizing_mode="stretch_both")
    plots.append(layout)

    return plots


# def draw_graph_step_standard(graph_df, step_times):
#     # print("graph_df", graph_df)
#     colors = Category10_10
#
#     plots = []
#     toggles = []
#     p = figure(title="Facility Graph", sizing_mode="scale_both", x_axis_label="Time", y_axis_label="Value", max_height=1000)
#     start_time = min(df["Time"].min() for df in graph_df)
#
#
#     for df in graph_df:
#         time_values = (df["Time"] - start_time).dt.total_seconds()
#         facility, column_name = df.columns[-1].split('-')
#
#         # 각 facility에 대한 step_times 가져오기
#         facility_step_times = step_times.get(facility, {})
#
#         color = colors[len(p.renderers) % len(colors)]
#
#         # Step별 BoxAnnotation 추가
#         for step, step_time in facility_step_times.items():
#
#             start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')  # Timestamp를 문자열로 변환
#             start_x = (pd.to_datetime(step_time['startTime']) - pd.to_datetime(start_time_str)).total_seconds()
#             end_x = (pd.to_datetime(step_time['endTime']) - pd.to_datetime(start_time_str)).total_seconds()
#             start_x -= time_values.min()
#             end_x -= time_values.min()
#
#             box_annotation = BoxAnnotation(left=start_x, right=end_x, fill_color=color, fill_alpha=0.1)
#             p.add_layout(box_annotation)
#
#             toggle = Toggle(label="box", button_type="success", active=True)
#             toggle.js_link('active', box_annotation, 'visible')
#             toggles.append(toggle)
#
#             # toggle = Toggle(label="box", button_type="success", active=True)
#             # toggle.js_link('active', box, 'visible')
#             # p.add_layout(toggle)
#
#             # toggle = Toggle(label=f"Box {step}", button_type="success", active=True)
#             # toggle.js_on_click(CustomJS(args=dict(annotation=box_annotation), code="""
#             #     annotation.visible = !annotation.visible;
#             # """))
#             # toggles.append(toggle)
#
#         time_values -= time_values.min()
#
#         source = ColumnDataSource(data={'Time': time_values, 'Value': df.iloc[:, -1]})
#         line = p.line(x='Time', y='Value', source=source, legend_label=f'{facility} - {column_name}', color=color)
#         hover = HoverTool(renderers=[line], tooltips=[
#             ('facility', f'{facility}'),
#             ('time', '@Time seconds'),
#             ('Value', '$y')
#         ])
#
#         p.add_tools(hover)
#
#     p.x_range.start = 0
#     p.xaxis.formatter = NumeralTickFormatter(format="0")
#     p.legend.location = "top_left"
#     p.toolbar.autohide = True
#     plots.append(p)
#
#     return plots

def draw_graph_step_standard(graph_df, step_times, batch_name_list):
    colors = Category10_10

    plots = []
    toggles = []
    tabs = []

    p = figure(title="Facility Graph", sizing_mode="scale_width", x_axis_label="Time", y_axis_label="Value", height=300)
    start_time = min(df["Time"].min() for df in graph_df)
    line_cnt = 0
    batch_cnt = 0
    for df in graph_df:
        line_cnt += 1
        time_values = (df["Time"] - start_time).dt.total_seconds()
        min_time = time_values.min()
        facility, column_name = df.columns[-1].split('-')
        batch_name = batch_name_list[batch_cnt]
        facility_step_times = step_times.get(facility+batch_name, {})
        batch_cnt += 1
        time_values -= time_values.min()

        color = colors[len(p.renderers) % len(colors)]

        df_toggles = []
        df_plots = []

        for step, step_time in facility_step_times.items():
            start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
            start_x = (pd.to_datetime(step_time['startTime']) - pd.to_datetime(start_time_str)).total_seconds()
            end_x = (pd.to_datetime(step_time['endTime']) - pd.to_datetime(start_time_str)).total_seconds()
            start_x -= min_time
            end_x -= min_time
            box_annotation = BoxAnnotation(left=start_x, right=end_x, fill_color=color, fill_alpha=0.1, visible=False)
            p.add_layout(box_annotation)

            toggle_label = f"{facility} - {column_name}- {step}"
            toggle1 = Toggle(label=toggle_label, button_type="default", active=False)
            toggle1.js_link('active',  box_annotation, 'visible')
            df_toggles.append(toggle1)

            step_df = df[(df["Time"] >= step_time['startTime']) & (df["Time"] <= step_time['endTime'])]
            min_value = step_df.iloc[:, -1].min()
            max_value = step_df.iloc[:, -1].max()
            std_deviation = step_df.iloc[:, -1].std()
            variance = step_df.iloc[:, -1].var()
            mean_value = step_df.iloc[:, -1].mean()
            median_value = step_df.iloc[:, -1].median()
            mode_value = step_df.iloc[:, -1].mode()

        df_plots.append(p)

        toggles.extend(df_toggles)
        source = ColumnDataSource(data={'Time': time_values, 'Value': df.iloc[:, -1]})
        line = p.line(x='Time', y='Value', source=source, legend_label=f'{facility} - {column_name}', color=color)
        hover = HoverTool(renderers=[line], tooltips=[
            ('facility', f'{facility}'),
            ('time', '@Time seconds'),
            ('Value', '$y')
        ])
        p.add_tools(hover)

        # CrosshairTool 생성
        width = Span(dimension="width", line_dash="dotted", line_width=1)
        height = Span(dimension="height", line_dash="dotted", line_width=1)
        p.add_tools(CrosshairTool(overlay=[width, height]))

        # tab = Panel(child=p, title=f"{facility} - {column_name}")
        # tabs.append(tab)
        # tabs0 = Tabs(tabs=[
        #     TabPanel(child=p, title="circle"),
        # ])
        # plots.append(tabs0)

    # DataTable 생성
    combined_df = pd.concat(graph_df)
    source = ColumnDataSource(combined_df)

    columns = [
        TableColumn(field=c, title=c) for c in combined_df.columns
    ]

    data_table = DataTable(source=source, columns=columns, editable=True, index_position=0, index_header="row",
                           sizing_mode="stretch_width")

    # 토글 버튼 테스트
    # toggle = Toggle(label="test", button_type="success", active=True)
    # toggle.js_link('active', line, 'visible')
    # tabs_obj = Tabs(tabs=tabs)

    p.x_range.start = 0
    p.xaxis.formatter = NumeralTickFormatter(format="0")
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    p.toolbar.autohide = True
    p.toolbar.logo = None

    # 그래프와 데이터 테이블을 수직으로 배치
    layout = column([p, data_table, row(toggles)], sizing_mode="stretch_both")
    plots.append(layout)

    return plots



def draw_detail_section_graph(graph_df, step_times):
    plots = []

    for df in graph_df:
        colors = Category10_10
        p = figure(title="Facility Graph", sizing_mode="scale_both", x_axis_label="Time", y_axis_label="Value", max_height=1000)
        start_time = min(df["Time"].min() for df in graph_df)
        time_values = (df["Time"] - start_time).dt.total_seconds()
        facility, column_name = df.columns[-1].split('-')

        facility_step_times = step_times.get(facility, {})

        color = colors[len(p.renderers) % len(colors)]

        for step, step_time in facility_step_times.items():
            start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
            start_x = (pd.to_datetime(step_time['startTime']) - pd.to_datetime(start_time_str)).total_seconds()
            end_x = (pd.to_datetime(step_time['endTime']) - pd.to_datetime(start_time_str)).total_seconds()
            start_x -= time_values.min()
            end_x -= time_values.min()

            box_annotation = BoxAnnotation(left=start_x, right=end_x, fill_color=color, fill_alpha=0.1)
            p.add_layout(box_annotation)

            # step_df = df[(df["Time"] >= step_time['startTime']) & (df["Time"] <= step_time['endTime'])]
            # min_value = step_df.iloc[:, -1].min()
            # max_value = step_df.iloc[:, -1].max()
            # std_deviation = step_df.iloc[:, -1].std()
            # variance = step_df.iloc[:, -1].var()
            # mean_value = step_df.iloc[:, -1].mean()
            # median_value = step_df.iloc[:, -1].median()
            # mode_value = statistics.mode(step_df.iloc[:, -1])

            # print(f"Step: {step}, Min: {min_value}, Max: {max_value}, Std Deviation: {std_deviation}, Variance: {variance}, Mean: {mean_value}, Median: {median_value}, Mode: {mode_value}")

        time_values -= time_values.min()

        color = colors[len(p.renderers) % len(colors)]
        source = ColumnDataSource(data={'Time': time_values, 'Value': df.iloc[:, -1]})
        line = p.line(x='Time', y='Value', source=source, legend_label=f'{facility} - {column_name}', color=color)
        hover = HoverTool(renderers=[line], tooltips=[
            ('facility', f'{facility}'),
            ('time', '@Time seconds'),
            ('Value', '$y')
        ])
        p.add_tools(hover)


    p.x_range.start = 0
    p.xaxis.formatter = NumeralTickFormatter(format="0")
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    p.toolbar.autohide = True

    plots.append(p)

    return plots




# 홀수번째에만 색칠
# def draw_graph_step_standard(graph_df, step_times):
#     # print("graph_df", graph_df)
#     colors = Category10_10
#
#     plots = []
#     toggles = []
#     p = figure(title="Facility Graph", sizing_mode="scale_both", x_axis_label="Time", y_axis_label="Value", max_height=1000)
#     start_time = min(df["Time"].min() for df in graph_df)
#
#     for df_index, df in enumerate(graph_df):
#         time_values = (df["Time"] - start_time).dt.total_seconds()
#         facility, column_name = df.columns[-1].split('-')
#
#         # 각 facility에 대한 step_times 가져오기
#         facility_step_times = step_times.get(facility, {})
#
#         color = colors[df_index % len(colors)]  # df_index가 홀수인 경우에만 색상 변경
#
#         # Step별 BoxAnnotation 추가
#         for step_index, (step, step_time) in enumerate(facility_step_times.items()):
#             if step_index % 2 == 0:  # step_index가 홀수인 경우에만 BoxAnnotation 추가
#                 start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')  # Timestamp를 문자열로 변환
#                 start_x = (pd.to_datetime(step_time['startTime']) - pd.to_datetime(start_time_str)).total_seconds()
#                 end_x = (pd.to_datetime(step_time['endTime']) - pd.to_datetime(start_time_str)).total_seconds()
#                 start_x -= time_values.min()
#                 end_x -= time_values.min()
#
#                 box_annotation = BoxAnnotation(left=start_x, right=end_x, fill_color=color, fill_alpha=0.1)
#                 p.add_layout(box_annotation)
#
#                 text = Label(x=(start_x + end_x) / 2, y=0, text=f"Step {step}", text_font_size="10pt",
#                              text_align="center", text_baseline="middle")
#                 p.add_layout(text)
#
#                 # toggle = Toggle(label="box", button_type="success", active=True)
#                 # toggle.js_link('active', box_annotation, 'visible')
#                 # toggles.append(toggle)
#
#                 # toggle = Toggle(label="box", button_type="success", active=True)
#                 # toggle.js_link('active', box, 'visible')
#                 # p.add_layout(toggle)
#
#                 # toggle = Toggle(label=f"Box {step}", button_type="success", active=True)
#                 # toggle.js_on_click(CustomJS(args=dict(annotation=box_annotation), code="""
#                 #     annotation.visible = !annotation.visible;
#                 # """))
#                 # toggles.append(toggle)
#
#         time_values -= time_values.min()
#
#         source = ColumnDataSource(data={'Time': time_values, 'Value': df.iloc[:, -1]})
#         line = p.line(x='Time', y='Value', source=source, legend_label=f'{facility} - {column_name}', color=color)
#         hover = HoverTool(renderers=[line], tooltips=[
#             ('facility', f'{facility}'),
#             ('time', '@Time seconds'),
#             ('Value', '$y')
#         ])
#
#         p.add_tools(hover)
#
#     p.x_range.start = 0
#     p.xaxis.formatter = NumeralTickFormatter(format="0")
#     p.legend.location = "top_left"
#     p.toolbar.autohide = True
#     plots.append(p)
#
#     return plots

# def draw_graph_step_standard(graph_df, end_time_list):
#     print("===============graph_df==================")
#     print(graph_df)
#     print("=========end_time_list==========")
#     print(end_time_list)
#     colors = Category10_10
#
#     plots = []
#     p = figure(title="Facility Graph", sizing_mode="scale_both", x_axis_label="Time", y_axis_label="Value", max_height=1000)
#
#     combined_df = pd.concat(graph_df)
#     start_time = pd.to_datetime(combined_df["Time"], utc=True).min()
#
#     for df in graph_df:
#         time_values = (pd.to_datetime(df["Time"], utc=True) - start_time).dt.total_seconds()
#         df["Time"] = time_values
#         facility, column_name = df.columns[-1].split('-')
#
#         color = colors[len(p.renderers) % len(colors)]
#         source = ColumnDataSource(data={'Time': time_values, 'Value': df.iloc[:, -1]})
#         line = p.line(x='Time', y='Value', source=source, legend_label=f'{facility} - {column_name}', color=color)
#         hover = HoverTool(renderers=[line], tooltips=[
#             ('facility', f'{facility}'),
#             ('time', '@Time seconds'),
#             ('Value', '$y')
#         ])
#
#         p.add_tools(hover)
#
#     p.x_range.start = 0
#     p.xaxis.formatter = NumeralTickFormatter(format="0")
#     p.legend.location = "top_left"
#     p.toolbar.autohide = True
#     plots.append(p)
#
#     return plots


# def draw_graph_step_standard(graph_df, end_time_list):
#
#     print("=============start===========")
#     print(end_time_list)
#     plots = []
#     p = figure(title="Facility Comparison", sizing_mode="scale_both", x_axis_label='Time (seconds)',
#                y_axis_label='Value',
#                height=400)
#
#     colors = Category10_10
#
#     print("====columns====")
#     print(graph_df.columns)
#     for i, df in enumerate(graph_df):
#         start_time = pd.to_datetime(df["Time"], utc=True).min()
#         df_name = facility_list[i]
#         df["Time"] = (pd.to_datetime(df["Time"], utc=True) - start_time).dt.total_seconds()
#
#         color = colors[i % len(colors)]
#         source = ColumnDataSource(data=df)
#
#         for j, column_name in enumerate(df.columns[1:]):
#             line = p.line(x='Time', y=column_name, source=source, legend_label=f"{df_name} - {column_name}",
#                           color=color)
#
#             hover = HoverTool(renderers=[line], tooltips=[
#                 ('facility', f'{df_name}'),
#                 ('time', '@Time seconds'),
#                 ('Value', '$y')
#             ])
#
#             # max_value, min_value, average = calc_df_values(source, df_name, column_name)
#             # average_line = Span(location=average, dimension='width', line_color=color, line_width=1)
#             # p.add_layout(average_line)
#             # average_hover = HoverTool(renderers=[line], tooltips=[
#             #     ('facility', f'{df_name}'),
#             #     ('Value', f'{average}')
#             # ])
#             # p.add_tools(average_hover)
#
#         p.add_tools(hover)
#
#         # # 최댓값과 최솟값 텍스트 추가
#         # p.text(x=[0], y=[0], text=[f'Min: {min_value}, Max: {max_value}'], text_font_size="10pt",
#         #        text_baseline="bottom", text_align="left", text_color="black")
#
#     p.x_range.start = 0
#     p.xaxis.formatter = NumeralTickFormatter(format="0")
#     p.legend.location = "top_left"
#     p.toolbar.autohide = True
#     plots.append(p)
#
#     return plots
#
# def draw_graph_time_standard(graph_df):
#     plots = []
#     p = figure(title="Facility Graph", sizing_mode="scale_width", x_axis_label="Time", y_axis_label="Value", max_height=1000)
#     colors = Category10_10
#
#     graph_df["Time"] = pd.to_datetime(graph_df["Time"], utc=True)
#
#     for column in graph_df.columns:
#         if column == "Time":
#             continue
#
#         facility, column_name = column.split("-")
#
#         color = colors[len(p.renderers) % len(colors)]
#         line = p.line(x="Time", y=column, source=graph_df, legend_label=f"{facility} - {column_name}", color=color)
#         hover = HoverTool(renderers=[line], tooltips=[
#                      ('facility', f'{column}'),
#                      ('time', '@Time{%F %T}'),
#                      ('Value', '$y')
#                  ], formatters={'@Time': 'datetime'})
#         p.add_tools(hover)
#
#     p.xaxis.formatter = DatetimeTickFormatter(hours='%H:%M:%S')
#     p.legend.location = "top_left"
#     p.toolbar.autohide = True
#     plots.append(p)
#
#     return plots


# def draw_graph_step_standard(graph_df, end_time_list):
#     print("=====================")
#     print(end_time_list)
#
#     plots = []
#     p = figure(title="Facility Graph", sizing_mode="scale_both", x_axis_label="Time", y_axis_label="Value", max_height=1000)
#     colors = Category10_10
#
#     print("graph_df", graph_df)
#     print("==============start_time=========")
#     start_time = graph_df["Time"].min()
#     graph_df["Time"] = (graph_df["Time"] - start_time).dt.total_seconds()
#
#     for column in graph_df:
#         if column == "Time":
#             continue
#
#         facility, column_name = column.split("-")
#         color = colors[len(p.renderers) % len(colors)]
#         line = p.line(x="Time", y=column, source=graph_df, legend_label=f"{facility} - {column_name}", color=color)
#
#         hover = HoverTool(renderers=[line], tooltips=[
#             ('facility', f'{column}'),
#             ('time', '@Time seconds'),
#             ('Value', '$y')
#         ])
#         p.add_tools(hover)
#
#     print(start_time)
#     idx = 1
#     for end_time in end_time_list:
#         end_time = pd.to_datetime(end_time)
#
#         end_time_seconds = (end_time- start_time).total_seconds()
#
#         print("end_time_seconds", end_time_seconds)
#
#         span = Span(location=end_time_seconds, dimension='height', line_color='black', line_dash='dashed', line_width=2)
#         p.add_layout(span)
#         print(idx, end_time)
#         idx += 1
#     p.x_range.start = 0
#     p.xaxis.formatter = NumeralTickFormatter(format="0")
#     p.legend.location = "top_left"
#     p.toolbar.autohide = True
#     plots.append(p)
#
#     return plots

# def draw_single_dataframe_to_graph(df, facility):
#
#     plots = []
#     all_data = []
#
#     time_values = pd.to_datetime(df["Time"], utc=True)
#
#     combined_data = dict(x=time_values)
#     for column in df.columns:
#         if column != "Time":
#             column_data = df[column]
#             all_data.append(column_data)
#             combined_data[column] = column_data.values
#
#     source = ColumnDataSource(data=combined_data)
#
#     p = figure(title="facility", sizing_mode="scale_both", x_axis_label='Time', y_axis_label='Value',
#                height=800)
#
#     for i, column_name in enumerate(df.columns[1:]):
#         line = p.line(x='x', y=column_name, source=source, legend_label=column_name, color=Category10_10[i])
#
#         hover = HoverTool(renderers=[line], tooltips=[
#             ('facility', f'{facility}'),
#             ('time', '@x{%H:%M:%S}'),
#             ('Value', '$y')
#         ],  formatters={'@x': 'datetime'})
#
#     p.add_tools(hover)
#
#     p.xaxis.formatter = DatetimeTickFormatter(hours='%H:%M:%S')
#     p.legend.location = "top_left"
#     p.toolbar.autohide = True
#     plots.append(p)
#
#     return plots
#
#
# def draw_multi_dataframe_to_graph(df_list, facility_list):
#     plots = []
#     p = figure(title="Facility Comparison", sizing_mode="scale_both", x_axis_label='Time (seconds)',
#                y_axis_label='Value',
#                height=400)
#
#     colors = Category10_10
#
#     for i, df in enumerate(df_list):
#         start_time = pd.to_datetime(df["Time"], utc=True).min()
#         df_name = facility_list[i]
#         df["Time"] = (pd.to_datetime(df["Time"], utc=True) - start_time).dt.total_seconds()
#
#         color = colors[i % len(colors)]
#         source = ColumnDataSource(data=df)
#
#         for j, column_name in enumerate(df.columns[1:]):
#             line = p.line(x='Time', y=column_name, source=source, legend_label=f"{df_name} - {column_name}",
#                           color=color)
#
#             hover = HoverTool(renderers=[line], tooltips=[
#                 ('facility', f'{df_name}'),
#                 ('time', '@Time seconds'),
#                 ('Value', '$y')
#             ])
#
#             # max_value, min_value, average = calc_df_values(source, df_name, column_name)
#             # average_line = Span(location=average, dimension='width', line_color=color, line_width=1)
#             # p.add_layout(average_line)
#             # average_hover = HoverTool(renderers=[line], tooltips=[
#             #     ('facility', f'{df_name}'),
#             #     ('Value', f'{average}')
#             # ])
#             # p.add_tools(average_hover)
#
#         p.add_tools(hover)
#
#         # # 최댓값과 최솟값 텍스트 추가
#         # p.text(x=[0], y=[0], text=[f'Min: {min_value}, Max: {max_value}'], text_font_size="10pt",
#         #        text_baseline="bottom", text_align="left", text_color="black")
#
#     p.x_range.start = 0
#     p.xaxis.formatter = NumeralTickFormatter(format="0")
#     p.legend.location = "top_left"
#     p.toolbar.autohide = True
#     plots.append(p)
#
#     return plots


def save_graph_data(graph_df):
    # print("=============save_graph_data==============")
    time_values = pd.to_datetime(graph_df["Time"], utc=True)
    y_data = {}
    for column in graph_df.columns:
        if column != "Time":
            y_data[column] = graph_df[column].values.tolist()
    print("========time_value==========")
    print(time_values)
    print("========y_data==========")
    print(y_data)
    # return time_values, y_data

    #
    #     for idx, df in enumerate(df_list):
    #         print(f"======DataFrame {idx + 1}======")
    #         print(df)
    #         print(df.columns)
    #         print("====time_values====")
    #         time_values = pd.to_datetime(df["Time"], utc=True)
    #         print(time_values)
    #
    #         combined_data = dict(x=time_values)
    #         y_data = {}
    #         for column in df.columns:
    #             if column != "Time":
    #                 column_data = df[column]
    #                 all_data.append(column_data)
    #                 combined_data[column] = column_data.values
    #                 if isinstance(column_data.values, np.ndarray):
    #                     y_data[column] = column_data.values.tolist()
    #
    #         source = ColumnDataSource(data=combined_data)
    #
    #         x_data = source.data['x']
    #         x_data_list.append(x_data)
    #         y_data_list.append(y_data)
    #
    #     print("=========x_data_list========")
    #     print(x_data_list)
    #     print("=========y_data_list========")
    #     print(y_data_list)
    #
    #     return [x_data_list, y_data_list, facility_list]

# def save_graph_data(df_list, facility_list):
#     # 선 하나만 추가할 때
#     if len(df_list) == 1:
#         return draw_single_line(df_list[0],facility_list[0])
#     else:
#         return draw_multi_line(df_list, facility_list)
#
# # 하나의 선 정보 저장
# def draw_single_line(df, facility):
#     print("===========method=============")
#     all_data = []
#     print(df)
#     print(df.columns)
#     print("====time_values====")
#     time_values = pd.to_datetime(df["Time"], utc=True)
#     print(time_values)
#
#     combined_data = dict(x=time_values)
#     y_data = {}
#     for column in df.columns:
#         if column != "Time":
#             column_data = df[column]
#             all_data.append(column_data)
#             combined_data[column] = column_data.values
#             if isinstance(column_data.values, np.ndarray):
#                 y_data[column] = column_data.values.tolist()
#
#     source = ColumnDataSource(data=combined_data)
#
#     x_data = source.data['x']
#     print("=========y_data========")
#     print(y_data)
#     print("=========y_data========")
#
#     return [x_data, y_data, facility]
#
# def draw_multi_line(df_list, facility_list):
#     print("===========method=============")
#     all_data = []
#     x_data_list = []
#     y_data_list = []
#
#     for idx, df in enumerate(df_list):
#         print(f"======DataFrame {idx + 1}======")
#         print(df)
#         print(df.columns)
#         print("====time_values====")
#         time_values = pd.to_datetime(df["Time"], utc=True)
#         print(time_values)
#
#         combined_data = dict(x=time_values)
#         y_data = {}
#         for column in df.columns:
#             if column != "Time":
#                 column_data = df[column]
#                 all_data.append(column_data)
#                 combined_data[column] = column_data.values
#                 if isinstance(column_data.values, np.ndarray):
#                     y_data[column] = column_data.values.tolist()
#
#         source = ColumnDataSource(data=combined_data)
#
#         x_data = source.data['x']
#         x_data_list.append(x_data)
#         y_data_list.append(y_data)
#
#     print("=========x_data_list========")
#     print(x_data_list)
#     print("=========y_data_list========")
#     print(y_data_list)
#
#     return [x_data_list, y_data_list, facility_list]
#

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

