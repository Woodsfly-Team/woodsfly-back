from fastapi import APIRouter
from fastapi.responses import FileResponse

website_router = APIRouter()

# 首页接口
@website_router.get("/")
async def read_index():
    return FileResponse("website/index.html")

@website_router.get("/page/{file_name}")
async def read_file(file_name: str):
    return FileResponse(f"website/{file_name}")
