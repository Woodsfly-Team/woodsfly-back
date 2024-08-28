from fastapi import APIRouter, Depends, FastAPI, UploadFile, File

from fastapi.responses import FileResponse

from sqlalchemy.orm import Session
import schemas
import crud
from database import get_db


website_router = APIRouter()

# 首页接口
@website_router.get("/")
async def read_index():
    return FileResponse("2125_artxibition/index.html")

@website_router.get("/{file_name}")
async def read_file(file_name: str):
    return FileResponse(f"2125_artxibition/{file_name}")
