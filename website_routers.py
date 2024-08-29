from fastapi import APIRouter
from fastapi.responses import FileResponse

website_router = APIRouter()
@website_router.get("/")
async def read_root():
    return FileResponse("website/index.html")


@website_router.get("/website/{file_name}")
async def read_file(file_name: str):
    return FileResponse(f"website/{file_name}")
