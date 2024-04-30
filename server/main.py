# fastapi
import uvicorn
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse

# bokeh
from bokeh.plotting import figure
from bokeh.embed import json_item

from app.routers.bokehgraph import bokeh_router
from app.routers.influx import influx_router

# postgreSQL
from database import engine
from psycopg2 import IntegrityError
from datetime import datetime, timedelta

# data frame
import pandas as pd
import numpy as np

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)