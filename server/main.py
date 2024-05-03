# fastapi
import uvicorn
from fastapi import FastAPI

# bokeh

from app.models.influx.influx_models import FacilityData
# section
from app.utils.functions.section import get_section_data

from app.routers.bokeh import bokeh_router
from app.routers.influx import influx_router
from app.routers.mongo import mongo_router

# postgreSQL

# data frame

# cors
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "*",
]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # cross-origin request에서 cookie를 포함할 것인지 (default=False)
    allow_methods=["*"],     # cross-origin request에서 허용할 method들을 나타냄. (default=['GET']
    allow_headers=["*"],     # cross-origin request에서 허용할 HTTP Header 목록
)

app.include_router(bokeh_router.router)
app.include_router(influx_router.influx_router)
app.include_router(mongo_router.mongo_router)

@app.post("/api/section")
async def section(conditon: FacilityData):
    print('conditon', conditon)
    return { "cycles": get_section_data(conditon) }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)