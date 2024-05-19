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
from bokeh.plotting import figure, show, output_file
from bokeh.transform import transform, linear_cmap
from bokeh.layouts import layout, column
from bokeh.palettes import Viridis256 as palette

from app.domain.correlation.model.correlation_section_data import CorrelationSectionData
from app.domain.facility.service.facility_function import get_correlation_datas


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

        section = CorrelationSectionData(
            facility=request_body.queryData[0].facility,
            batchName=request_body.queryData[0].batchName,
            parameter=request_body.queryData[0].parameter,
            startTime=start_time,
            endTime=end_time
        )

        df = get_correlation_datas(section)
        print("df:", df)
        print("\n\ndf.columns:", df.columns)
        if (len(df) == 0):
            return None

        # 상관 관계
        # df_numeric = df.select_dtypes(include=[np.number])
        # df_numeric.fillna(0, inplace=True)
        # df = df_numeric.corr()

        # 산점도
        fig = plt.figure(figsize=(20, 20))
        # corr_feature = df.corr(method='pearson')
        # corr_feature = df.corr(method='spearman')
        corr_feature = df.corr(method='kendall')

        feature = df.columns.tolist()
        n_feature = len(feature)

        for i in range(n_feature):
            for j in range(n_feature):
                ax = fig.add_subplot(n_feature, n_feature, i * n_feature + j + 1)
                plt.scatter(df[feature[j]], df[feature[i]], s=9)

                if i == 0:
                    ax.xaxis.tick_top()
                    ax.xaxis.set_label_position('top')
                    plt.xlabel(feature[j], fontsize=12)
                if j == 0:
                    plt.ylabel(feature[i], fontsize=12)
                ax.annotate(np.round(corr_feature.loc[feature[i], feature[j]], 3), xy=(1, 0),
                            xycoords='axes fraction', fontsize=16,
                            horizontalalignment='right', verticalalignment='bottom')

        # 산점도 저장
        fig.savefig('scatter_plot.png', dpi=300)
        plt.close(fig)  # 현재의 figure 닫기

        # 히트맵 저장
        plt.figure(figsize=(10, 8))
        h = sns.heatmap(corr_feature, annot=True, fmt=".4f", cmap='coolwarm', cbar=True)
        plt.title('Feature Correlation Heatmap')
        h.xaxis.tick_top()
        h.xaxis.set_label_position('top')
        plt.xticks(rotation=45)
        plt.yticks(rotation=0)
        plt.savefig('heatmap.png', dpi=300)
        plt.close()  # 현재의 figure 닫기

        # 출력 파일 설정
        output_file("correlation_plots.html")

        # 산점도 이미지 표시
        p1 = figure(width=800, height=800, toolbar_location=None)
        p1.image_url(url=['scatter_plot.png'], x=0, y=1, w=1, h=1)
        p1.xaxis.visible = False
        p1.yaxis.visible = False
        p1.xgrid.grid_line_color = None
        p1.ygrid.grid_line_color = None

        # 히트맵 이미지 표시
        p2 = figure(width=800, height=640, toolbar_location=None)
        p2.image_url(url=['heatmap.png'], x=0, y=1, w=1, h=1)
        p2.xaxis.visible = False
        p2.yaxis.visible = False
        p2.xgrid.grid_line_color = None
        p2.ygrid.grid_line_color = None

        # 레이아웃 설정
        layout = column(p1, p2)

        # 표시
        show(layout)

        plots.append(layout)

        return plots

    elif request_body.queryType == 'step':
        print("\n\nstep인 경우")

        return None