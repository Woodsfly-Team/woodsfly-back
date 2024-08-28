from fastapi import APIRouter
from fastapi.responses import FileResponse

website_router = APIRouter()

# 首页接口
@website_router.get("/")
async def read_index():
    return FileResponse("2125_artxibition/index.html")

@website_router.get("/page/{file_name}")
async def read_file(file_name: str):
    return FileResponse(f"2125_artxibition/{file_name}")
