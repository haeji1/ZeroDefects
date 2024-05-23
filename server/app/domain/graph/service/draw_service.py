# bokeh
from bokeh.embed import json_item
from pprint import pprint

import numpy as np
from bokeh.layouts import column, layout
from bokeh.models import (TableColumn, DataTable, CrosshairTool, Tabs, TabPanel, Div, MultiChoice, CustomJS, LabelSet)

from bokeh.models import (DatetimeTickFormatter, HoverTool, ColumnDataSource, Range1d, BoxAnnotation)
from bokeh.models.formatters import NumeralTickFormatter
from bokeh.models import Span
from bokeh.palettes import Category10_10
from bokeh.plotting import figure

# data frame
import pandas as pd
from starlette.responses import JSONResponse


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
    plot_list = []
    setting_options = extract_setting_values(request)
    setting_infos = make_setting_lines(request)
    setting_multi_choice = MultiChoice(value=["settings"], options=setting_options, placeholder='Settings')

    colors = Category10_10
    plots = []
    tabs = []
    tab_list = []
    toggle_labels = []
    box_annotations = []
    lines = []
    plot_lines = []

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

        plot_list.append(plot)

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

    # P에 SetValue 관련 모든 선 추가
    plot_lines_list = [[] for _ in range(len(plot_list))]
    for i in range(len(setting_infos)):
        start_x_time = start_second[i]
        end_x_time = end_second[i]
        for j in range(len(setting_infos[i])):
            setting_color = colors[len(p.renderers) % len(colors)]
            step_x_range = np.arange(start_x_time, end_x_time + 1)
            step_x_range = pd.Series(step_x_range)
            line_source = ColumnDataSource(data={'Time': step_x_range, 'Value': step_x_range})
            line = p.line(x='Time', y=setting_infos[i][j], source=line_source, color=setting_color, visible=False)
            for k in range(len(plot_list)):
                plot_info = plot_list[k]
                line2 = plot_list[k].line(x='Time', y=setting_infos[i][j], source=line_source, color=setting_color, visible=False)
                plot_lines.append(line2)
                plot_lines_list[k].append(line2)

                hover4 = HoverTool(renderers=[line2], tooltips=[
                    ('Setting', '$y'),
                    ('Duration', '@Time seconds'),
                ])
                plot_info.add_tools(hover4)
            lines.append(line)

            # setvalue hover 추가
            hover3 = HoverTool(renderers=[line], tooltips=[
                ('Setting', '$y'),
                ('Duration', '@Time seconds'),
            ])

            p.add_tools(hover3)


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
    setting_multi_choice_title = Div(text="""<h3>Choose Settings</h3>""", width=400, height=30)
    multi_choice_title = Div(text="""<h3>Choose Steps</h3>""", width=400, height=30)
    tab_title =  Div(text="""<h2>Graph</h2>""", width=400, height=40)
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
    setting_multi_choice_plots_callback = CustomJS(
        args=dict(setting_multi_choice=setting_multi_choice, plot_lines_list=plot_lines_list, setting_options=setting_options), code="""
        const selected = setting_multi_choice.value;
        for (let i = 0; i < setting_options.length; i++) {
            for (let j = 0; j < plot_lines_list.length; j++) {
                const plot_lines = plot_lines_list[j];
                if (selected.includes(setting_options[i])) {
                    plot_lines[i].visible = true;
                } else {
                    plot_lines[i].visible = false;
                }
            }
        }
    """
    )
    setting_multi_choice.js_on_change("value", setting_multi_choice_callback,setting_multi_choice_plots_callback)

    layout_1 = layout(
    [
                [setting_multi_choice_title],
                [setting_multi_choice],
                [multi_choice_title],
                [multi_choice],
                [tab_title],
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
    time_info = []
    setting_step_and_values = []
    for i in range(len(request)):
        step_length = len(request[i]['steps'])
        for j in range(step_length):
            min_start_val = request[i].get('steps', [])[0].keys()
            first_key = list(min_start_val)[0]
            if first_key == 'Step0':
                step_values = request[i]['steps'][j]
                step_columns = step_values[f'Step{j}']
            else:
                step_values = request[i]['steps'][j]
                step_columns = step_values[f'Step{j + 1}']
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
                else:
                    # 안에 있는 최종 키들 (Step1-ICP-ICP1, Step1-TG1-Power)
                    step_column_info = list(sorted(step_columns[column_key].keys()))
                    for l in range(len(step_column_info)):
                        info_name = step_column_info[l]
                        value = step_columns[column_key][info_name]
                        step_values_list.append(value)
            setting_step_and_values.append(step_values_list)

    return setting_step_and_values


def draw_TGLife_default_graph(df, tg_num):
    plots = []
    # metrics = ['section', 'count', 'sum', 'avg', 'max', 'min']
    # colors = ['skyblue', 'green', 'red', 'purple', 'orange', 'brown']
    metrics = ['section', 'avg']
    colors = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
        '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
        '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5'
    ]
    sections = [f'step{i}' for i in range(20)]
    scatters = [[] for _ in range(len(sections))]
    df_sorted = df.sort_values(by='section', ascending=True)
    multi_choice = MultiChoice(options=sections, placeholder='Steps')
    p = figure(title="Facility Comparison", sizing_mode="scale_width", min_width=800, height=200)

    # 섹션별로 데이터프레임 그룹화
    grouped = df_sorted.groupby('section')
    for section, group in grouped:
        section_index = int(section) # 섹션 인덱스를 정수로 변환
        for i, metric in enumerate(metrics[1:], start=1):  # 섹션을 제외한 나머지 메트릭에 대해 반복
            source = ColumnDataSource(data={f'TG{tg_num}Life[kWh]': group[f'TG{tg_num}Life[kWh]'], metric: group[metric]})
            # scatter = p.scatter(x=f'TG{tg_num}Life[kWh]', y=metric, source=source, color=colors[i - 1], size=10,
            #                     legend_label=metric, visible=False)
            scatter = p.scatter(x=f'TG{tg_num}Life[kWh]', y=metric, source=source, color=colors[section_index],
                                alpha=0.7, size=10, legend_label=metric, visible=True)

            hover = HoverTool(renderers=[scatter], tooltips=[
                ('Tg', '$x'),
                ('Value', '$y')
            ])
            p.add_tools(hover)
            if section_index < 20:
                scatters[section_index].append(scatter)  # 섹션 번호에 해당하는 리스트에 scatter 추가

            # CrosshairTool 생성
            width = Span(dimension="width", line_dash="dotted", line_width=1)
            height = Span(dimension="height", line_dash="dotted", line_width=1)
            p.add_tools(CrosshairTool(overlay=[width, height]))

    # p.legend.click_policy = "hide"
    p.toolbar.autohide = True
    p.toolbar.logo = None

    tg_multi_choice_callback = CustomJS(
        args=dict(multi_choice=multi_choice, scatters=scatters, sections=sections), code="""
            const selected = multi_choice.value;
            const noSelected = selected.length === 0;
            
            for (let i = 0; i < sections.length; i++) {
                const section_scatter = scatters[i]
                for (let j = 0; j < section_scatter.length; j++) {
                    if (noSelected || selected.includes(sections[i])) {
                        section_scatter[j].visible = true;
                    } else {
                        section_scatter[j].visible = false;
                    }
                }
            }
    """)

    multi_choice.js_on_change("value", tg_multi_choice_callback)

    layout1 = layout(
    [
            [p],
            [multi_choice]
        ],
        sizing_mode="stretch_width",
    )
    plots.append(layout1)
    plot_json = [json_item(plot, f'TG{tg_num}Life[kWh]') for plot in plots]
    return JSONResponse(plot_json)
