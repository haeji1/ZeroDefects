import os
from dotenv import load_dotenv
from pymongo import MongoClient
from app.models.influx.influx_models import FacilityData
from app.utils.functions.influx_functions import get_section
from app.models.section.section_models import BatchInfo, FacilityInfo

load_dotenv()

url = os.getenv('MONGO_FURL')
client = MongoClient(url)
db = client["section"]


# 파일이 업로드되면 파일의 전 구간에서 배치와 사이클 구간 찾아서 MongoDB에 저장
def save_section_data(facility: str, condition: FacilityData):
    df = get_section(condition)

    # 배치 및 스텝 시작과 끝 인덱스 저장을 위한 리스트
    batch_starts = []
    batch_ends = []
    step_starts = []  # 각 스텝의 시작 인덱스
    step_ends = []  # 각 스텝의 끝 인덱스
    current_step = None  # 현재 스텝

    step_number = 0  # 스텝 번호

    # 'RcpReq[]' 컬럼과 'CoatingLayerN[Layers]' 컬럼을 기준으로 배치 및 스텝의 시작과 끝 찾기
    for i in range(len(df)):

        # 배치 시작 검사
        if df['RcpReq[]'][i] == 1:
            if i == 0 or (i > 0 and df['RcpReq[]'][i - 1] == 0):
                batch_starts.append(i)
                current_step = 0  # 배치가 시작되면 스텝을 0으로 초기화
                step_starts.append(i)  # 스텝 시작 인덱스 추가
                step_number = 0  # 스텝 번호를 0으로 초기화
            # 스텝 변경 검사 (CoatingLayerN[Layers] 값의 변화를 기준으로 스텝 구분)
            elif df['CoatingLayerN[Layers]'][i] != df['CoatingLayerN[Layers]'][i - 1]:
                step_ends.append(i - 1)  # 이전 스텝의 끝 인덱스를 추가
                step_starts.append(i)  # 새로운 스텝의 시작 인덱스를 추가
                step_number += 1  # 스텝 번호 증가
        else:
            if i > 0 and df['RcpReq[]'][i - 1] == 1:
                # 배치가 끝나는 지점 처리
                batch_ends.append(i - 1)
                step_ends.append(i - 1)  # 현재 스텝의 끝 인덱스 추가
                current_step = None  # 스텝 초기화

    # 마지막 배치의 끝 처리
    if df['RcpReq[]'].iloc[-1] == 1:
        batch_ends.append(len(df) - 1)
        step_ends.append(len(df) - 1)  # 마지막 스텝의 끝 처리

    equipment_name = facility

    # JSON 구조 생성
    output = {"batches": []}

    batch_list = []
    section_list = []

    # 각 배치 및 스텝의 이름 생성 및 출력
    for batch_start, batch_end in zip(batch_starts, batch_ends):
        batch_name = f"batch-{equipment_name}-{df['Time'][batch_start]}"
        batch_dict = {
            "batch_name": batch_name,
            "batch_start_time": df['Time'][batch_start],
            "batch_end_time": df['Time'][batch_end],
            "steps": []
        }

        # 해당 배치 내의 스텝들 출력
        step_index = 0
        steps_dict = []
        for start, end in zip(step_starts, step_ends):
            if start >= batch_start and end <= batch_end:
                step_dict = {
                    f"step{step_index}": {
                        f"step{step_index}StartTime": df['Time'][start].strftime('%Y-%m-%d %H:%M:%S'),
                        f"step{step_index}EndTime": df['Time'][end].strftime('%Y-%m-%d %H:%M:%S')
                    }
                }
                batch_dict["steps"].append(step_dict)
                step_index += 1

                steps_dict.append(step_dict)

        try:
            section_list.append(BatchInfo(batchName=batch_name,
                                          batchStartTime=df['Time'][batch_start].strftime('%Y-%m-%d %H:%M:%S'),
                                          batchEndTime=df['Time'][batch_end].strftime('%Y-%m-%d %H:%M:%S'),
                                          steps=steps_dict))
        except TypeError as e:
            print(f"Error appending to batch_list: {e}")

    # section_list를 mongodb에 저장
    section = db[facility]
    for s in section_list:
        section.insert_one(dict(s))


def get_batches_info(facility: FacilityInfo) -> []:
    # facility를 기반으로 해당 컬렉션 선택
    collection = db[facility.facility]

    # 컬렉션에서 모든 문서(배치 정보) 조회
    batches = list(collection.find({}))

    # MongoDB의 ObjectId를 문자열로 변환 (선택적)
    for batch in batches:
        batch.pop('_id', None)  # '_id' 키가 있으면 제거하고, 없으면 아무 일도 하지 않음
        batch.pop('steps', None)  # 'steps' 키가 있으면 제거하고, 없으면 아무 일도 하지 않음
    return batches
