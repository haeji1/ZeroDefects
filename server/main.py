# fastapi
import uvicorn
from fastapi import FastAPI

from app.domain.facility.controller import facility_controller
from app.domain.graph.controller import graph_controller
from app.domain.recipe.controller import recipe_controller
from app.domain.section.controller import batch_controller

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

app.include_router(graph_controller.graph_router)
app.include_router(facility_controller.facility_router)
app.include_router(batch_controller.section_router)
app.include_router(recipe_controller.recipe_router)
