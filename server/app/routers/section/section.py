import os
from typing import List

import pandas as pd
import json

from dotenv import load_dotenv
from pymongo import MongoClient

from app.routers.influx.influx_model import FacilityData
from app.routers.influx.influx_utils import influx_get_all_data
from app.routers.section.section_models import Cycle
from app.routers.section.section_models import CycleSection

load_dotenv()
url = os.getenv('MONGO_FURL')

# MongoDB client
client = MongoClient(url)

db = client["section"]

def get_section_data(condition: FacilityData) -> [CycleSection]:

    df = influx_get_all_data(condition)

    # 사이클 및 스텝 시작과 끝 인덱스 저장을 위한 리스트
    cycle_starts = []
    cycle_ends = []
    step_starts = []  # 각 스텝의 시작 인덱스
    step_ends = []  # 각 스텝의 끝 인덱스
    current_step = None  # 현재 스텝
    step_number = 0  # 스텝 번호

    # 'RcpReq[]' 컬럼과 'CoatingLayerN[Layers]' 컬럼을 기준으로 사이클 및 스텝의 시작과 끝 찾기
    for i in range(len(df)):

        # 사이클 시작 검사
        if df['RcpReq[]'][i] == 1:
            if i == 0 or (i > 0 and df['RcpReq[]'][i - 1] == 0):
                cycle_starts.append(i)
                current_step = 0  # 사이클이 시작되면 스텝을 0으로 초기화
                step_starts.append(i)  # 스텝 시작 인덱스 추가
                step_number = 0  # 스텝 번호를 0으로 초기화
            # 스텝 변경 검사 (CoatingLayerN[Layers] 값의 변화를 기준으로 스텝 구분)
            elif df['CoatingLayerN[Layers]'][i] != df['CoatingLayerN[Layers]'][i - 1]:
                step_ends.append(i - 1)  # 이전 스텝의 끝 인덱스를 추가
                step_starts.append(i)  # 새로운 스텝의 시작 인덱스를 추가
                step_number += 1  # 스텝 번호 증가
        else:
            if i > 0 and df['RcpReq[]'][i - 1] == 1:
                # 사이클이 끝나는 지점 처리
                cycle_ends.append(i - 1)
                step_ends.append(i - 1)  # 현재 스텝의 끝 인덱스 추가
                current_step = None  # 스텝 초기화

    # 마지막 사이클의 끝 처리
    if df['RcpReq[]'].iloc[-1] == 1:
        cycle_ends.append(len(df) - 1)
        step_ends.append(len(df) - 1)  # 마지막 스텝의 끝 처리

    # 파일명에서 설비명과 날짜 추출
    # equipment_name, log_type, date, log_start_time = file_path.split('-')
    equipment_name = condition.facility

    # JSON 구조 생성
    output = {"cycles": []}

    cycle_list = []
    section_list = []

    # 각 사이클 및 스텝의 이름 생성 및 출력
    for cycle_start, cycle_end in zip(cycle_starts, cycle_ends):
        cycle_name = f"cycle-{equipment_name}-{df['Time'][cycle_start][0:19]}"
        cycle_dict = {
            "cycle_name": cycle_name,
            "cycle_start_time": df['Time'][cycle_start],
            "cycle_end_time": df['Time'][cycle_end],
            "steps": []
        }

        # 해당 사이클 내의 스텝들 출력
        step_index = 0
        steps_dict = []
        for start, end in zip(step_starts, step_ends):
            if start >= cycle_start and end <= cycle_end:
                step_dict = {
                    f"step{step_index}": {
                        "start_time": df['Time'][start],
                        "end_time": df['Time'][end]
                    }
                }
                cycle_dict["steps"].append(step_dict)
                step_index += 1

                steps_dict.append(step_dict)

        output["cycles"].append(cycle_dict)

        try:
            cycle_list.append(Cycle(cycleName=cycle_name,
                                    cycleStartTime=df['Time'][cycle_start],
                                    cycleEndTime=df['Time'][cycle_end]))

            section_list.append(CycleSection(cycleName=cycle_name,
                                             cycleStartTime=str(df['Time'][cycle_start]), cycleEndTime=str(df['Time'][cycle_end]),
                                             steps=steps_dict))
        except TypeError as e:
            print(f"Error appending to cycle_list: {e}")

    # section_list 를 mongodb에 저장
    print(condition.facility)
    section = db[condition.facility]
    for s in section_list:
        print(dict(s))
        section.insert_one(dict(s))

    return cycle_list