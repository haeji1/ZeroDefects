import os
from typing import List

import pymongo
from bokeh.embed import json_item
from dotenv import load_dotenv
from fastapi import HTTPException
from pymongo import MongoClient, ReplaceOne
from starlette.responses import JSONResponse

from app.domain.facility.model.facility_data import FacilityData
from app.domain.facility.service.facility_function import get_datas
from app.domain.graph.service.draw_service import draw_dataframe_to_graph
from app.domain.section.model.batch_info import BatchInfo
from app.domain.section.model.faciltiy_info import FacilityInfo
from app.domain.section.model.graph_query_request import GraphQueryRequest
from app.domain.section.model.section_data import SectionData

load_dotenv()

url = os.getenv('MONGO_FURL')
client = MongoClient(url)
db = client["section"]


# 파일이 업로드되면 파일의 전 구간에서 배치와 사이클 구간 찾아서 MongoDB에 저장
def save_section_data(facility: str, df):
    # 배치 및 스텝 시작과 끝 인덱스 저장을 위한 리스트
    batch_starts = []
    batch_ends = []
    step_starts = []  # 각 스텝의 시작 인덱스
    step_ends = []  # 각 스텝의 끝 인덱스

    step_number = 0  # 스텝 번호

    # 'RcpReq[]' 컬럼과 'CoatingLayerN[Layers]' 컬럼을 기준으로 배치 및 스텝의 시작과 끝 찾기
    for i in range(len(df)):
        # 배치 시작 검사
        if df['RcpReq[]'][i] == 1:
            if i == 0 or (i > 0 and df['RcpReq[]'][i - 1] == 0):
                batch_starts.append(i)
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

    # 마지막 배치의 끝 처리
    if df['RcpReq[]'].iloc[-1] == 1:
        batch_ends.append(len(df) - 1)
        step_ends.append(len(df) - 1)  # 마지막 스텝의 끝 처리

    equipment_name = facility

    section_list = []

    # 각 배치 및 스텝의 이름 생성 및 출력
    for batch_start, batch_end in zip(batch_starts, batch_ends):
        batch_name = f"batch-{equipment_name}-{df['DateTime'][batch_start]}"
        batch_dict = {
            "batch_name": batch_name,
            "batch_start_time": df['DateTime'][batch_start],
            "batch_end_time": df['DateTime'][batch_end],
            "steps": []
        }

        # 해당 배치 내의 스텝들 출력
        step_index = 0
        steps_dict = []
        for start, end in zip(step_starts, step_ends):
            if start >= batch_start and end <= batch_end:
                step_dict = {
                    f"step{step_index}": {
                        f"step{step_index}StartTime": df['DateTime'][start].strftime('%Y-%m-%d %H:%M:%S'),
                        f"step{step_index}EndTime": df['DateTime'][end].strftime('%Y-%m-%d %H:%M:%S')
                    }
                }
                batch_dict["steps"].append(step_dict)
                step_index += 1

                steps_dict.append(step_dict)

        try:
            section_list.append(BatchInfo(batchName=batch_name,
                                          batchStartTime=df['DateTime'][batch_start].strftime('%Y-%m-%d %H:%M:%S'),
                                          batchEndTime=df['DateTime'][batch_end].strftime('%Y-%m-%d %H:%M:%S'),
                                          steps=steps_dict))
        except TypeError as e:
            print(f"Error appending to batch_list: {e}")

    # MongoDB에 배치 정보 저장
    operations = [ReplaceOne({'batchName': s.batchName}, dict(s), upsert=True) for s in section_list]
    if operations:
        db[facility].bulk_write(operations)


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


def read_from_section(request_body: List[FacilityData]):
    results = []
    for item in request_body:
        collection_name = item['facility']  # collection 이름은 facility 값
        cycle_name = item['cycleName']
        step = item.get('step')  # step이 None일 수도 있으므로 get 메소드 사용

        collection = db[collection_name]  # 해당 facility의 컬렉션 선택

        # cycle_name이 있는 경우
        if cycle_name:
            cycle_query = {"cycles.cycle_name": cycle_name}
            cycle_data = collection.find_one(cycle_query)

            if cycle_data:
                for cycle in cycle_data['cycles']:
                    if cycle['cycle_name'] == cycle_name:
                        if step is None:  # step이 None이면 cycle의 시간 정보를 가져옴
                            results.append({
                                "cycle_start_time": cycle['cycle_start_time'],
                                "cycle_end_time": cycle['cycle_end_time']
                            })
                        else:  # step이 지정된 경우 해당 step의 시간 정보를 가져옴
                            step_key = f"step{step}"
                            for step_item in cycle['steps']:
                                if step_key in step_item:
                                    results.append(step_item[step_key])
                                    break
                        break

    return JSONResponse(status_code=200, content=results)


def draw_graph(request_body: GraphQueryRequest):
    if request_body.queryType == "time":
        sections: List[SectionData] = []
        for data in request_body.queryData:
            sections.append(SectionData(
                facility=data.facility,
                batchName=data.batchName,
                parameter=data.parameter,
                startTime=request_body.queryCondition.startTime,
                endTime=request_body.queryCondition.endTime
            ))
            print('sections ', sections)
            facility_list, parameter_list, df_list = get_datas(sections)
            plots = draw_dataframe_to_graph(df_list, facility_list)
            plot_json = [json_item(plot, f"my_plot_{idx}") for idx, plot in enumerate(plots)]

        return JSONResponse(status_code=200, content=plot_json)
    elif request_body.queryType == "step":
        sections = get_sections_info(request_body)
        if not sections:
            raise HTTPException(status_code=404, detail="Sections not found")
        return {"sections": sections}
    else:
        raise HTTPException(status_code=404, detail="queryType must be 'time' or 'step'")


def get_sections_info(request_body: GraphQueryRequest) -> []:
    responses = []

    for data in request_body.queryData:
        print("data:", data)
        collection = db[data.facility]
        batch_document = collection.find_one({"batchName": data.batchName})
        print(batch_document)
        if not batch_document:
            raise HTTPException(status_code=404, detail=f"Batch {data.batchName} not found in {data.facility}")

        steps = request_body.queryCondition.step
        if not steps:
            raise HTTPException(status_code=400, detail="Invalid step range")

        start_time = None
        end_time = None

        start_step_key = f"step{steps[0]}"
        end_step_key = f"step{steps[-1]}"
        for step_item in batch_document['steps']:
            if start_step_key in step_item:
                start_time = step_item[start_step_key][f"{start_step_key}StartTime"]
            if end_step_key in step_item:
                end_time = step_item[end_step_key][f"{end_step_key}EndTime"]

        if start_time is None or end_time is None:
            raise HTTPException(status_code=404, detail="No step in batch")

        response = {
            "facility": data.facility,
            "batchName": data.batchName,
            "parameter": data.parameter,
            "startTime": start_time,
            "endTime": end_time
        }
        responses.append(response)

    return responses


def get_step_info_using_facility_name_on_mongoDB(request_body):
    result = []
    # mongodb collection setting으로 변경
    db = client["setting"]

    # 스텝값 구하기
    steps = request_body.queryCondition.step

    # 딕셔너리 만들기
    # facilityName(id느낌), batchName에 대한 key 및 value 넣기
    for r in request_body.queryData:
        d = {}
        for key, val in r:
            if key == "facility":
                d["facilityName"] = val
            elif key == "batchName":
                d["batchName"] = val
        result.append(d)

    # 스텝 찾아서 넣기
    for val in result:
        facility_name = val["facilityName"]
        # 가장 최근 레시피 가져오겠다.
        collections = list(db[facility_name].find().sort('_id', -1).limit(1))
        # 스텝 리스트 넣을 리스트
        step_list= []
        for item in collections:
            for step in steps:
                step_key = f"Step{step}"
                step_list.append({step_key: item[step_key]})
        val["steps"] = step_list

    # for facility_name in facility_names:
    #     result[facility_name].append({"steps": []})
    # for name in facility_names:
    #     collections = list(db[name].find().sort('_id', -1).limit(1))
    #     for i in collections:
    #         for step in steps:
    #             # = i["steps"][step]
    #             print(result[name][1])

    return result
