import pandas as pd
import json

def get_section_data(filename):
    # CSV 파일 경로 설정
    file_path = filename

    # CSV 파일 읽기
    df = pd.read_csv(file_path)

    # 날짜 시간 형식 변환 ('Time' 컬럼에 대해)
    df['Time'] = pd.to_datetime(df['Time']).dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-7] + 'Z'
    # df['Time'] = pd.to_datetime(df['Time'], format='%y-%m-%d %H:%M:%S').dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-7] + 'Z'

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
    equipment_name, log_type, date, log_start_time = file_path.split('-')

    # JSON 구조 생성
    output = {"cycles": []}

    # 각 사이클 및 스텝의 이름 생성 및 출력
    for cycle_start, cycle_end in zip(cycle_starts, cycle_ends):
        cycle_name = f"cycle-{equipment_name}-{date}-{df['Time'][cycle_start]}"
        cycle_dict = {
            "cycle_name": cycle_name,
            "cycle_start_time": df['Time'][cycle_start],
            "cycle_end_time": df['Time'][cycle_end],
            "steps": []
        }

        # 해당 사이클 내의 스텝들 출력
        step_index = 0
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

        output["cycles"].append(cycle_dict)

    # JSON 출력
    # print(json.dumps(output, indent=4, ensure_ascii=False))