from fastapi import APIRouter, File, UploadFile
from starlette.responses import JSONResponse

from typing import List

from app.domain.facility.model.facility_data import TGLifeData, TGLifeModel, RequestTGLifeInfo, RequestTGConditions
from app.domain.facility.service.influx_client import InfluxGTRClient
from app.domain.facility.service.facility_function import get_facilities_info, get_TG_datas, get_TG_cycles_info
from app.domain.graph.service.draw_service import draw_TGLife_default_graph

from config import settings

url = settings.influx_url
token = settings.influx_token
organization = settings.influx_org
bucket = settings.influx_bucket

facility_router = APIRouter(prefix="/facility", tags=['request'])


@facility_router.post("/write")
async def write_influxdb(files: List[UploadFile] = File(...)):
    client = InfluxGTRClient(url=url, token=token, org=organization, bucket_name=bucket)
    contents = await client.write_csv(files)

    return JSONResponse(status_code=200, content=contents)


# for test
@facility_router.get("/info")
async def get_info_test():
    contents = get_facilities_info()
    if contents is None:
        return JSONResponse(status_code=404, content={"message": "No facilities info"})
    else:
        return JSONResponse(status_code=200, content=contents)

@facility_router.post("/tg/info")
async def get_TG_info(condition: RequestTGLifeInfo):
    contents = get_TG_cycles_info(condition)
    if contents is None:
        return JSONResponse(status_code=404, content={"message": "No facilities info"})
    else:
        return JSONResponse(status_code=200, content=contents)

@facility_router.post("/read/tg")
async def read_tg_influxdb(model: RequestTGConditions):
    life_models = []
    for queryCondition in model.queryConditions:
        life_model = TGLifeData(
            type='time',
            facility=model.queryData.facility,
            tgLifeNum=model.queryData.tgLifeNum,
            parameter=model.queryData.parameter,
            statistics=model.queryData.statistics,
            cycleName=queryCondition.cycleName,
            startTime=queryCondition.startTime,
            endTime=queryCondition.endTime
        )
        life_models.append(life_model)

    try:
        contents = get_TG_datas(life_models)
        if contents is None:
            return JSONResponse(status_code=400, content={'msg': 'not exist data'})
        else:
            return draw_TGLife_default_graph(contents, model)
            # return JSONResponse(status_code=200, content={'msg': })
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content={'msg': str(e)})

# for test
# @facility_router.post("/read/tg")
# async def read_tg_influxdb(model: TGLifeModel):
#
#     life_model = TGLifeData(
#         type=model.queryType,
#         facility=model.queryData.facility,
#         tgLifeNum=model.queryData.tgLifeNum,
#         startTime=model.queryCondition.startTime,
#         endTime=model.queryCondition.endTime,
#         startCnt=model.queryCondition.startCnt,
#         endCnt=model.queryCondition.endCnt
#     )
#
#     try:
#         contents = get_TG_datas(life_model)
#         if contents is None:
#             return JSONResponse(status_code=400, content={'msg': 'not exist data'})
#         else:
#             return draw_TGLife_default_graph(contents, model.queryData.tgLifeNum)
#             # return JSONResponse(status_code=200, content={'msg': })
#     except Exception as e:
#         print(e)
#         return JSONResponse(status_code=400, content={'msg': str(e)})