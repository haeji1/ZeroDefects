# bokeh
from bokeh.models import (ColumnDataSource, DatetimeTickFormatter, HoverTool)
from bokeh.models.formatters import NumeralTickFormatter
from bokeh.palettes import Category10_10
from bokeh.plotting import figure

# data frame
import pandas as pd


def draw_dataframe_to_graph(df_list, facility_list):

    if len(df_list) == 1:
        return draw_single_dataframe_to_graph(df_list[0])
    else:
        plots = []
        p = figure(title="Facility Comparison", sizing_mode="stretch_width", x_axis_label='Time (seconds)',
                   y_axis_label='Value',
                   height=400)

        colors = Category10_10

        for i, df in enumerate(df_list):

            start_time = pd.to_datetime(df["Time"].str.replace("Z", ""), utc=True).min()
            df_name = facility_list[i]
            df["Time"] = (pd.to_datetime(df["Time"].str.replace("Z", ""), utc=True) - start_time).dt.total_seconds()
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

            p.add_tools(hover)

        p.x_range.start = 0
        p.xaxis.formatter = NumeralTickFormatter(format="0")
        p.legend.location = "top_left"
        plots.append(p)

        return plots


def draw_single_dataframe_to_graph(df):

    plots = []
    all_data = []

    df["Time"] = df["Time"].str.replace("Z", "")
    time_values = pd.to_datetime(df["Time"], utc=True)

    combined_data = dict(x=time_values)
    for column in df.columns:
        if column != "Time":
            column_data = df[column]
            all_data.append(column_data)
            combined_data[column] = column_data.values

    source = ColumnDataSource(data=combined_data)

    p = figure(title="facility", x_axis_label='Time', y_axis_label='Value',
               width=1200, height=400)

    for i, column_name in enumerate(df.columns[1:]):
        p.line(x='x', y=column_name, source=source, legend_label=column_name, color=Category10_10[i])

    p.xaxis.formatter = DatetimeTickFormatter(hours='%H:%M:%S')
    p.legend.location = "top_left"
    plots.append(p)

    return plots

