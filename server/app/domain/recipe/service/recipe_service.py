from datetime import datetime

from fastapi import HTTPException
from pymongo import MongoClient
from fastapi.responses import JSONResponse
import pandas as pd

from app.domain.facility.service.facility_utils import get_measurement_code
from config import settings

url = settings.mongo_furl

# MongoDB client
client = MongoClient(url)
# database name is setting
setting = client["setting"]


def recipe_service(files):
    # read setting_facility.xls files
    responses = []
    for file in files:
        if not file.filename.endswith('.xls') and not file.filename.endswith('.xlsx'):
            responses.append({"filename": file.filename, "message": "Invalid file format"})
            continue

        try:
            df = pd.read_excel(file.file, header=None)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        df.loc[25:44, 3:78] = df.loc[25:44, 3:78].fillna(0)
        facility_before = file.filename.split('_')[1].split('.')[0]
        facility = get_measurement_code(facility_before)
        # db collection name is facility(from file_name)
        collection = setting[facility]
        data_to_insert = {}

        # select datas
        for i in range(0, 21):
            step_key = f"Step{i}"
            data_to_insert[step_key] = {
                "Time": df.iloc[25 + i][3],
                "TG1": {
                    "Power": df.iloc[25 + i][4],
                    "Ar1": df.iloc[25 + i][6],
                    "Ar2": df.iloc[25 + i][8],
                    "Ar3": df.iloc[25 + i][10],
                    "Ar4": df.iloc[25 + i][12]
                },
                "TG2": {
                    "Power": df.iloc[25 + i][14],
                    "Ar1": df.iloc[25 + i][16],
                    "Ar2": df.iloc[25 + i][18],
                    "Ar3": df.iloc[25 + i][20],
                    "Ar4": df.iloc[25 + i][22]
                },
                "TG4": {
                    "Power": df.iloc[25 + i][34],
                    "Ar1": df.iloc[25 + i][36],
                    "Ar2": df.iloc[25 + i][38],
                    "Ar3": df.iloc[25 + i][40],
                    "Ar4": df.iloc[25 + i][42]
                },
                "TG5": {
                    "Power": df.iloc[25 + i][44],
                    "Ar1": df.iloc[25 + i][46],
                    "Ar2": df.iloc[25 + i][48],
                    "Ar3": df.iloc[25 + i][50],
                    "Ar4": df.iloc[25 + i][52]
                },
                "ICP": {
                    "ICP1": df.iloc[25 + i][64],
                    "ICP2": df.iloc[25 + i][66],
                    "ICP3": df.iloc[25 + i][68],
                    "ICP4": df.iloc[25 + i][70],
                    "Ar": df.iloc[25 + i][72],
                    "O2A": df.iloc[25 + i][74],
                    "O2B": df.iloc[25 + i][76],
                    "N2": df.iloc[25 + i][78]
                }
            }

        # 현재 날짜와 시간을 추가
        data_to_insert['last_updated'] = datetime.now()

        try:
            data_list = [data_to_insert]  # 딕셔너리를 리스트 안에 넣어줌
            if data_list:
                # upsert=True 옵션을 사용하여 문서가 없으면 삽입하고, 이미 있으면 업데이트합니다.
                # 문서를 구별할 수 있는 고유한 키 "facility_name" 사용
                collection.update_one({"facility_name": facility}, {"$set": data_to_insert}, upsert=True)
                responses.append(
                    {"filename": file.filename, "message": "File uploaded and data inserted/updated successfully!"})
            else:
                responses.append({"filename": file.filename, "message": "No documents to insert"})
        except Exception as e:
            responses.append({"filename": file.filename, "message": str(e)})

    return JSONResponse(status_code=200, content=responses)