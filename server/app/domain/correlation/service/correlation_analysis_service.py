import base64
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from bokeh.models import Div, TabPanel, Tabs, DataTable, TableColumn, ColumnDataSource
from bokeh.layouts import column

from app.domain.correlation.model.correlation_section_data import CorrelationSectionData
from app.domain.facility.service.facility_function import get_correlation_datas


# 이미지 파일을 Base64로 인코딩하는 함수
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


# 산점도 함수
def plot_scatter(df, corr_feature, method_name):
    feature = df.columns.tolist()
    n_feature = len(feature)
    fig = plt.figure(figsize=(20, 20))
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
    scatter_plot_path = f'scatter_plot_{method_name}.png'
    fig.savefig(scatter_plot_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    return scatter_plot_path


# 히트맵 함수
def plot_heatmap(corr_feature, method_name):
    plt.figure(figsize=(10, 8))
    h = sns.heatmap(corr_feature, annot=True, fmt=".4f", cmap='coolwarm', cbar=True, vmin=-1, vmax=1)
    h.xaxis.tick_top()
    h.xaxis.set_label_position('top')
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    heatmap_path = f'heatmap_{method_name}.png'
    plt.savefig(heatmap_path, dpi=300, bbox_inches='tight')
    plt.close()
    return heatmap_path


# 탭 생성 함수
def create_tab(df, method):
    # 상관 계수
    corr_feature = df.corr(method=method)

    scatter_plot_path = plot_scatter(df, corr_feature, method)
    heatmap_path = plot_heatmap(corr_feature, method)

    encoded_scatter_plot = encode_image_to_base64(scatter_plot_path)
    encoded_heatmap = encode_image_to_base64(heatmap_path)

    scatter_plot_title = Div(text=f"<h2>Scatter Plot ({method})</h2>", width=400, height=30)
    heatmap_title = Div(text=f"<h2>Heat Map ({method})</h2>", width=400, height=30)
    raw_data_table_title = Div(text=f"<h2>Raw Data ({method})</h2>", width=400, height=30)

    scatter_plot_div = Div(
        text=f'<img src="data:image/png;base64,{encoded_scatter_plot}" alt="scatter_plot" width="800" height="800">',
        sizing_mode="stretch_width", margin=20)

    heatmap_div = Div(
        text=f'<img src="data:image/png;base64,{encoded_heatmap}" alt="heatmap" width="800" height="600">',
        sizing_mode="stretch_width", margin=20)

    # Raw Data Table
    source = ColumnDataSource(df)
    columns = [
        TableColumn(field=c, title=c) for c in df.columns
    ]
    raw_data_table = DataTable(source=source, columns=columns, editable=False, index_position=0, index_header="row",
                               sizing_mode="stretch_width", margin=20)

    return TabPanel(child=column(scatter_plot_title, scatter_plot_div, heatmap_title, heatmap_div, raw_data_table_title
                                 , raw_data_table), title=f'Correlation Coefficient({method})')


def analyze_correlation(request_body):
    plots = []
    if request_body.queryType == "time":
        # 표준시로 변경
        start_time = datetime.strptime(request_body.queryCondition.startTime, "%Y-%m-%dT%H:%M:%S.%fZ")
        start_time += timedelta(hours=9)
        start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        end_time = datetime.strptime(request_body.queryCondition.endTime, "%Y-%m-%dT%H:%M:%S.%fZ")
        end_time += timedelta(hours=9)
        end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        section = CorrelationSectionData(
            facility=request_body.queryData.facility,
            batchName=request_body.queryData.batchName,
            parameter=request_body.queryData.parameter,
            startTime=start_time,
            endTime=end_time
        )

        df = get_correlation_datas(section)
        print("df:", df)
        print("\n\ndf.columns:", df.columns)
        if len(df) == 0:
            return None

        # 상관 관계
        df = df.select_dtypes(include=[np.number])
        df.fillna(0, inplace=True)

        tabs = [create_tab(df, method) for method in ['pearson', 'spearman', 'kendall']]
        plots.append(Tabs(tabs=tabs))

        return plots

    elif request_body.queryType == 'step':
        return plots
