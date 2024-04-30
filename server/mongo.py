from fastapi import FastAPI, File, UploadFile, HTTPException
from pymongo import MongoClient
from fastapi.responses import JSONResponse
import pandas as pd

app = FastAPI()

# MongoDB client
client = MongoClient("mongodb://admin:Delos@localhost:27017/")
# database name is setting
setting = client["setting"]

@app.post("/setting")
async def upload_excel_file(files: list[UploadFile] = File(...)):
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
        facility = file.filename.split('_')[1].split('.')[0]
        # db collection name is facility(from file_name)
        collection = setting[facility]
        data_to_insert = {}

        # select datas
        for i in range(0, 21):
            step_key = f"Step{i}"
            data_to_insert[step_key] = {
                "Time": df.iloc[25+i][3],
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

        try:
            data_list = [data_to_insert]  # 딕셔너리를 리스트 안에 넣어줌
            if data_list:
                collection.insert_many(data_list)  # insert_many 메서드에 리스트 형식의 데이터 전달
                responses.append(
                    {"filename": file.filename, "message": "File uploaded and data inserted successfully!"})
            else:
                responses.append({"filename": file.filename, "message": "No documents to insert"})
        except Exception as e:
            responses.append({"filename": file.filename, "message": str(e)})

    return JSONResponse(status_code=200, content=responses)

# mongodb read test
@app.put("/point")
def update_point():
    test = client["test"]
    testedtest = test["testedtest"]
    john_doe_doc = testedtest.find_one({"name": "John Doe"})
    if john_doe_doc:
        email = john_doe_doc.get("email")
        return {"email": email}
    else:
        return {"message": "John Doe의 도큐먼트를 찾을 수 없습니다."}
