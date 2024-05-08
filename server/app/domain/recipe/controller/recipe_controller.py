from fastapi import APIRouter, File, UploadFile
from app.domain.recipe.service import recipe_service


recipe_router = APIRouter(prefix="/facility", tags=['setting'])


@recipe_router.post("/setting")
async def upload_excel_file(files: list[UploadFile] = File(...)):
    return recipe_service.recipe_service(files)