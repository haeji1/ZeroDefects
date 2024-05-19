# bokeh
from bokeh.embed import json_item
from pprint import pprint

import numpy as np
from bokeh.layouts import column, layout, gridplot
from bokeh.models import (TableColumn, DataTable, Toggle, CrosshairTool, Tabs, TabPanel, Div, MultiChoice,
                          CheckboxGroup, Dropdown, TextInput, CustomJS)

from bokeh.models import (DatetimeTickFormatter, HoverTool, ColumnDataSource, Range1d, BoxAnnotation)
from bokeh.models.formatters import NumeralTickFormatter
from bokeh.models import Span
from bokeh.palettes import Category10_10
from bokeh.plotting import figure

# data frame
import pandas as pd


def draw_dataframe_to_graph(graph_type, graph_df, steps_times_info=None, batch_name_list=None, request=None):
    if graph_type == "time":
        return draw_graph_time_standard(graph_df)
    elif graph_type == "step":
        return draw_graph_step_standard(graph_df, steps_times_info, batch_name_list, request)


def draw_graph_time_standard(graph_df):
    # print("graph_df =", graph_df)
    if (len(graph_df) == 0):
        return []

    colors = Category10_10

    tabs = []
    tab_list = []
    plots = []
    statistics_list = []

    p = figure(title="Facility Comparison", sizing_mode="scale_width", x_axis_label='Time',
               y_axis_label='Value', height=300)

    for df in graph_df:
        plot = figure(title="Facility Graph", sizing_mode="scale_width", x_axis_label="Time", y_axis_label="Value",
                      min_width=1200, height=300)

        facility, column_name = df.columns[-1].split('-')
        # 통계값 추출
        min_value = df.iloc[:, -1].min()
        max_value = df.iloc[:, -1].max()
        std_value = df.iloc[:, -1].std()
        variance = df.iloc[:, -1].var()
        mean_value = df.iloc[:, -1].mean()
        median_value = df.iloc[:, -1].median()
        mode_value = df.iloc[:, -1].mode()

        data = {
            'facility': facility + column_name,
            'MinValue': min_value,
            'MaxValue': max_value,
            'StdValue': std_value,
            'Variance': variance,
            'MeanValue': mean_value,
            'MedianValue': median_value,
            'ModeValue': mode_value
        }
        statistics_list.append(data)

        time_values = pd.to_datetime(df['Time'], utc=True)
        df["Time"] = pd.to_datetime(df["Time"])


        color = colors[len(p.renderers) % len(colors)]
        source = ColumnDataSource(data={'Time': time_values, 'Value': df[df.columns[-1]]})
        line = p.line(x='Time', y='Value', source=source, legend_label=f'{facility} - {column_name}', color=color)
        line2 = plot.line(x='Time', y='Value', source=source, legend_label=f'{facility} - {column_name}', color=color)

        hover = HoverTool(renderers=[line], tooltips=[
                     ('facility', f'{facility}'),
                     ('time', '@Time{%F %T}'),
                     ('Value', '$y')
                 ], formatters={'@Time': 'datetime'})

        hover2 = HoverTool(renderers=[line2], tooltips=[
            ('facility', f'{facility}'),
            ('time', '@Time{%F %T}'),
            ('Value', '$y')
        ], formatters={'@Time': 'datetime'})

        p.add_tools(hover)
        plot.add_tools(hover2)
        plot.xaxis.formatter = DatetimeTickFormatter(hours='%Y-%m-%d %H:%M:%S')
        plot.legend.location = "top_left"
        plot.legend.click_policy = "hide"
        plot.toolbar.logo = None

        # CrosshairTool 생성
        width = Span(dimension="width", line_dash="dotted", line_width=1)
        height = Span(dimension="height", line_dash="dotted", line_width=1)
        p.add_tools(CrosshairTool(overlay=[width, height]))
        plot.add_tools(CrosshairTool(overlay=[width, height]))

        tab_list.append(TabPanel(child=plot, title=f'{column_name}'))

    statistics_df = pd.DataFrame(statistics_list)
    datasource = ColumnDataSource(statistics_df)
    columns = [
        TableColumn(field=s, title=s) for s in statistics_df.columns
    ]

    # Statistics Table
    statistics_table = DataTable(source=datasource, columns=columns, index_position=0,
                                 index_header="row", sizing_mode="stretch_width")
    # Raw Data Table
    combined_df = pd.concat(graph_df)
    combined_df['Time'] = pd.to_datetime(combined_df['Time'], unit='s')
    combined_df['Time'] = combined_df['Time'].dt.strftime('%Y-%m-%d %H:%M:%S')
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

    tabs.append(TabPanel(child=p, title="All Facilities"))
    for tab in tab_list:
        tabs.append(tab)

    data_table_title = Div(text="""<h2>Raw Data</h2>""", width=400, height=30)
    statistics_table_title = Div(text="""<h2>Statistics</h2>""", width=400, height=30)

    layout_1 = layout(
        [
                [Tabs(tabs=tabs)],
                [data_table_title],
                [data_table],
                [statistics_table_title],
                [statistics_table],
            ],

        sizing_mode="stretch_width",
    )
    plots.append(layout_1)

    return plots


def draw_graph_step_standard(graph_df, step_times, batch_name_list, request):
    start_second = []
    end_second = []
    setting_options = extract_setting_values(request)
    lines_info, setting_infos = make_setting_lines(request)
    x_range_times_for_lines = []

    setting_multi_choice = MultiChoice(value=["settings"], options=setting_options, placeholder='Settings')

    colors = Category10_10
    plots = []
    tabs = []
    tab_list = []
    toggle_labels = []
    box_annotations = []
    lines = []

    p = figure(title="Facility Comparison", sizing_mode="scale_width", x_axis_label="Time", y_axis_label="Value", min_width=800, height=200)

    start_time = min(df["Time"].min() for df in graph_df)
    batch_cnt = 0
    data_list = []
    for df in graph_df:
        plot = figure(title="Facility Comparison", sizing_mode="scale_width", x_axis_label="Time", y_axis_label="Value", min_width=800, height=200)

        time_values = (df["Time"] - start_time).dt.total_seconds()
        min_time = time_values.min()
        facility, column_name = df.columns[-1].split('-')
        batch_name = batch_name_list[batch_cnt]
        facility_step_times = step_times.get(facility+batch_name, {})
        facility_step_total = list(facility_step_times.keys())
        for i in range (len(facility_step_total)):
            x_range_times_for_lines.append(facility_step_times[facility_step_total[i]])
        batch_cnt += 1
        time_values -= time_values.min()

        color = colors[len(p.renderers) % len(colors)]
        step_x_range_list = []

        for step, step_time in facility_step_times.items():
            start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
            start_x = (pd.to_datetime(step_time['startTime']) - pd.to_datetime(start_time_str)).total_seconds()
            end_x = (pd.to_datetime(step_time['endTime']) - pd.to_datetime(start_time_str)).total_seconds()
            start_x -= min_time
            end_x -= min_time
            box_annotation = BoxAnnotation(left=start_x, right=end_x, fill_color=color, fill_alpha=0.1, visible=False)
            p.add_layout(box_annotation)
            plot.add_layout(box_annotation)
            box_annotations.append(box_annotation)
            step_x_range_list.append({step: step, start_x: start_x, end_x: end_x})
            start_second.append(start_x)
            end_second.append(end_x)

            toggle_label = f"{batch_name} - {step}"
            toggle_labels.append(toggle_label)

            step_df = df[(df["Time"] >= step_time['startTime']) & (df["Time"] <= step_time['endTime'])]
            min_value = step_df.iloc[:, -1].min()
            max_value = step_df.iloc[:, -1].max()
            std_deviation = step_df.iloc[:, -1].std()
            variance = step_df.iloc[:, -1].var()
            mean_value = step_df.iloc[:, -1].mean()
            median_value = step_df.iloc[:, -1].median()
            mode_value = step_df.iloc[:, -1].mode()

            data = {
                'facility': f'{column_name} - {batch_name}',
                'Step': step,
                'MinValue': min_value,
                'MaxValue': max_value,
                'StdValue': std_deviation,
                'Variance': variance,
                'MeanValue': mean_value,
                'MedianValue': median_value,
                'ModeValue': mode_value
            }
            data_list.append(data)

        source = ColumnDataSource(data={'Time': time_values, 'Value': df.iloc[:, -1]})
        line = p.line(x='Time', y='Value', source=source, legend_label=f'{column_name} - {batch_name}', color=color)
        line2 = plot.line(x='Time', y='Value', source=source, legend_label=f'{column_name} - {batch_name}', color=color)

        hover = HoverTool(renderers=[line], tooltips=[
            ('facility', f'{facility}'),
            ('time', '@Time seconds'),
            ('Value', '$y')
        ])
        p.add_tools(hover)
        hover2 = HoverTool(renderers=[line2], tooltips=[
            ('facility', f'{facility}'),
            ('time', '@Time seconds'),
            ('Value', '$y')
        ])
        plot.add_tools(hover2)
        plot.legend.location = "top_left"
        plot.legend.click_policy = "hide"
        plot.toolbar.logo = None

        # CrosshairTool 생성
        width = Span(dimension="width", line_dash="dotted", line_width=1)
        height = Span(dimension="height", line_dash="dotted", line_width=1)
        p.add_tools(CrosshairTool(overlay=[width, height]))

        tab_list.append(TabPanel(child=plot, title=f'{column_name} - {batch_name}'))

    statistics_df = pd.DataFrame(data_list)
    datasource = ColumnDataSource(statistics_df)
    columns = [
        TableColumn(field=s, title=s) for s in statistics_df.columns
    ]

    # Statistics Table
    statistics_table = DataTable(source=datasource, columns=columns, index_position=0,
                                 index_header="row", sizing_mode="stretch_width")

    # Raw Data Table
    combined_df = pd.concat(graph_df)
    combined_df['Time'] = pd.to_datetime(combined_df['Time'], unit='s')
    combined_df['Time'] = combined_df['Time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    source = ColumnDataSource(combined_df)

    columns = [
        TableColumn(field=c, title=c) for c in combined_df.columns
    ]
    data_table = DataTable(source=source, columns=columns, editable=False, index_position=0, index_header="row",
                           sizing_mode="stretch_width")

    # # P에 SetValue 관련 모든 선 추가
    for i in range(len(setting_infos)):
        start_x_time = start_second[i]
        end_x_time = end_second[i]
        for j in range(len(setting_infos[i])):
            step_x_range = np.arange(start_x_time, end_x_time + 1)
            step_x_range = pd.Series(step_x_range)
            line_source = ColumnDataSource(data={'Time': step_x_range, 'Value': step_x_range})
            line = p.line(x='Time', y=setting_infos[i][j], source=line_source, color=color, visible=False)
            lines.append(line)

    p.x_range.start = 0
    p.xaxis.formatter = NumeralTickFormatter(format="0")
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    p.toolbar.autohide = True
    p.toolbar.logo = None

    tabs.append(TabPanel(child=p, title="All Facilities"))
    for tab in tab_list:
        tabs.append(tab)

    data_table_title = Div(text="""<h2>Raw Data</h2>""", width=400, height=30)
    statistics_table_title = Div(text="""<h2>Statistics</h2>""", width=400, height=30)

    print("toggle_labels:", toggle_labels)

    multi_choice = MultiChoice(options=toggle_labels, placeholder='Steps')
    multi_choice_callback = CustomJS(
        args=dict(multi_choice=multi_choice, box_annotations=box_annotations, toggle_labels=toggle_labels), code="""
        const selected = multi_choice.value;  // 현재 선택된 값
        for (let i = 0; i < toggle_labels.length; i++) {
            if (selected.includes(toggle_labels[i])) {
                console.log(toggle_labels[i]);
                box_annotations[i].visible = true;
            } else {
                box_annotations[i].visible = false;
            }
        }
    """)
    multi_choice.js_on_change("value", multi_choice_callback)

    setting_multi_choice_callback = CustomJS(
        args=dict(setting_multi_choice=setting_multi_choice, lines=lines, setting_options=setting_options), code="""
        const selected = setting_multi_choice.value;
        for (let i = 0; i < setting_options.length; i++) {
            if (selected.includes(setting_options[i])) {
                console.log(setting_options[i]);
                lines[i].visible = true;
                } else {
                    lines[i].visible = false;
                }
            }
    """)
    setting_multi_choice.js_on_change("value", setting_multi_choice_callback)

    layout_1 = layout(
    [
                [setting_multi_choice],
                [multi_choice],
                # [grid],
                [Tabs(tabs=tabs)],
                # [toggles],
                [data_table_title],
                [data_table],
                [statistics_table_title],
                [statistics_table],
            ],

        sizing_mode="stretch_width",
    )

    plots.append(layout_1)
    return plots

def extract_setting_values(request):
    options = []
    for i in range(len(request)):
        step_length = len(request[i]['steps'])
        for j in range(step_length):
            min_start_val = request[i].get('steps', [])[0].keys()
            first_key = list(min_start_val)[0]
            if first_key == 'Step0':
                step_number = f"Step{j}"
                step_values = request[i]['steps'][j]
                step_columns = step_values[f'Step{j}']
            else:
                step_number = f"Step{j + 1}"
                step_values = request[i]['steps'][j]
                step_columns = step_values[f'Step{j + 1}']
            facility = request[i]['facilityName']
            # 각 step별 column들의 key값 (Step1-ICP, Step1-TG1...) 일 때 [ICP, TG1...]
            step_column_keys = list(sorted(step_columns.keys()))
            for k in range(len(step_column_keys)):
                # step별 column의 key값 리스트에서 뽑은 key값(Step1-ICP, Step1-TG1...)
                column_key = step_column_keys[k]
                # column_key가 Time이면 시간 정보만 담겨있음
                if column_key != "Time":
                    # 안에 있는 최종 키들 (Step1-ICP-ICP1, Step1-TG1-Power)
                    step_column_info = list(sorted(step_columns[column_key].keys()))
                    for l in range(len(step_column_info)):
                        info_name = step_column_info[l]
                        select_name = (f"{facility}-{step_number}-{column_key}-{info_name}")
                        options.append(select_name)
    return options

def make_setting_lines(request):
    # pprint(request)
    # pprint(request)
    setting_info = []
    time_info = []
    setting_values = []
    setting_step_and_values = []
    step_time = None
    for i in range(len(request)):
        step_length = len(request[i]['steps'])
        for j in range(step_length):
            min_start_val = request[i].get('steps', [])[0].keys()
            first_key = list(min_start_val)[0]
            if first_key == 'Step0':
                step_number = f"Step{j}"
                step_values = request[i]['steps'][j]
                step_columns = step_values[f'Step{j}']
            else:
                step_number = f"Step{j + 1}"
                step_values = request[i]['steps'][j]
                step_columns = step_values[f'Step{j + 1}']
            facility = request[i]['facilityName']
            # 각 step별 column들의 key값 (Step1-ICP, Step1-TG1...) 일 때 [ICP, TG1...]
            step_column_keys = list(sorted(step_columns.keys()))
            # step별로 리스트로 한 번 더 감싸기
            step_values_list = []
            for k in range(len(step_column_keys)):
                # step별 column의 key값 리스트에서 뽑은 key값(Step1-ICP, Step1-TG1...)
                column_key = step_column_keys[k]
                # column_key가 Time이면 시간 정보만 담겨있음
                if column_key == "Time":
                    step_time = step_columns['Time']
                    time_info.append(step_time)
                    # print(time_info)
                else:
                    # 안에 있는 최종 키들 (Step1-ICP-ICP1, Step1-TG1-Power)
                    step_column_info = list(sorted(step_columns[column_key].keys()))
                    # pprint(step_column_info)
                    for l in range(len(step_column_info)):
                        info_name = step_column_info[l]
                        # pprint(step_columns[column_key][info_name])
                        value = step_columns[column_key][info_name]
                        setting_values.append(value)
                        setting_info.append({"Time": step_time, "Value": value})
                        # setting_step_and_values.append(({"Step": step_number, 'Value': value}))
                        # step_values_list.append({"Step": step_number, 'Value': value})
                        step_values_list.append(value)
            setting_step_and_values.append(step_values_list)
    # pprint(setting_step_and_values)
    # print(len(setting_step_and_values))
    # print(setting_step_and_values[0])

    return setting_values, setting_step_and_values


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
    p.toolbar.logo = None

    plots.append(p)

    return plots

def draw_TGLife_default_graph(df, tg_num):
    print('=======df=======')
    print(df)

    plots = []
    p = figure(width=1200, height=600)
    p.line(x=df[f'TG{tg_num}Life[kWh]'], y=df['count'], line_color="red")
    p.line(x=df[f'TG{tg_num}Life[kWh]'], y=df[f'AVG-P.TG{tg_num}V[V]'], line_color="blue")
    p.line(x=df[f'TG{tg_num}Life[kWh]'], y=df[f'AVG-P.TG{tg_num}I[A]'], line_color="green")

    # box1 = BoxAnnotation(left=8620, right=8630, fill_color="red", fill_alpha=0.1)
    # box2 = BoxAnnotation(left=8625, right=8635, fill_color="blue", fill_alpha=0.1)
    # p.add_layout(box1)
    # p.add_layout(box2)

    bokeh_layout = column(p, sizing_mode="stretch_both")
    plots.append(bokeh_layout)

    return json_item(bokeh_layout)
