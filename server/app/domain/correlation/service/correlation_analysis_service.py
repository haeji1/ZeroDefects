import base64
from datetime import datetime, timedelta
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from bokeh.embed import components
from bokeh.models import LinearColorMapper, ColorBar, BasicTicker, PrintfTickFormatter, ColumnDataSource, TableColumn, \
    DataTable, Div
from bokeh.plotting import figure
from bokeh.transform import transform, linear_cmap
from bokeh.layouts import layout

from app.domain.facility.service.facility_function import get_correlation_datas
from app.domain.section.model.section_data import SectionData


def analyze_correlation(request_body):
    plots = []
    if request_body.queryType == "time":
        print("\n\ntime인 경우")

        # 표준시로 변경
        start_time = datetime.strptime(request_body.queryCondition.startTime, "%Y-%m-%dT%H:%M:%S.%fZ")
        start_time += timedelta(hours=9)
        start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        end_time = datetime.strptime(request_body.queryCondition.endTime, "%Y-%m-%dT%H:%M:%S.%fZ")
        end_time += timedelta(hours=9)
        end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        section = SectionData(
            facility=request_body.queryData[0].facility,
            batchName=request_body.queryData[0].batchName,
            parameter=request_body.queryData[0].parameter,
            startTime=start_time,
            endTime=end_time
        )

        df = get_correlation_datas(section)
        # print("df:", df)
        # print("\n\ndf.columns:", df.columns)
        if (len(df) == 0):
            return None

        feature = ['P.PEG201Press[Pa]', 'P.DG201Press[Pa]', 'RcpReq[]', 'CurrentCoatingCount[]']
        df = df[feature]

        correlation_matrix = df.corr()

        # 모든 feature 간의 산점도 생성
        plot_path = 'plot.png'
        sns.pairplot(df)
        plt.show()
        plt.savefig(plot_path)
        plt.close()

        # 히트맵 생성
        heatmap_path = 'heatmap.png'
        sns.heatmap(correlation_matrix, annot=True, vmin=-1, vmax=1)
        # plt.show()
        plt.savefig(heatmap_path)
        plt.close()

        # plt.figure(figsize=(10, 8))
        # sns.heatmap(correlation_matrix, annot=True, fmt=".4f", cmap='coolwarm', cbar=True)
        # plt.title('Feature Correlation Heatmap')
        # plt.xticks(rotation=45)
        # plt.yticks(rotation=0)
        # plt.show()

        # # 상관계수 데이터 준비
        # x = list(correlation_matrix.columns)
        # y = list(correlation_matrix.index)
        # colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]
        # # mapper = LinearColorMapper(palette=colors, low=-1, high=1)
        #
        # # Bokeh 도표 생성
        # plot = figure(title="Correlation Coefficient HeatMap", x_range=x, y_range=list(reversed(y)),
        #               x_axis_location="above", sizing_mode="scale_width", width=900, height=400)
        #
        # # 히트맵 생성을 위한 데이터 소스 준비
        # data_source = correlation_matrix.stack().reset_index()
        # data_source.columns = ['x', 'y', 'image']
        #
        # # 히트맵 생성
        # r = plot.rect(x="x", y="y", width=1, height=1, source=data_source, line_color=None,
        #               fill_color=linear_cmap("image", colors, low=-1, high=1))
        #
        # plot.add_layout(r.construct_color_bar(
        #     major_label_text_font_size="7px",
        #     ticker=BasicTicker(desired_num_ticks=len(colors)),
        #     formatter=PrintfTickFormatter(format="%d%%"),
        #     label_standoff=6,
        #     border_line_color=None,
        #     padding=5,
        # ), 'right')

        layout1 = layout(
            [
                # [plot]
                # [correlation_graph]
            ],

            sizing_mode="stretch_width",
        )

        plots.append(layout1)

        return plots

    elif request_body.queryType == 'step':
        print("\n\nstep인 경우")

        return None