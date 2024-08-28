from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas
import crud
from database import get_db

user_router = APIRouter()

# 创建用户接口
@user_router.put("/user")
async def user_create(username: str, password: str, db: Session = Depends(get_db)):
    if crud.username_has_exist(db, username):  # 用户名已存在
        data = None
        return schemas.CustomResponse(code=400, message="用户名已存在", data=data)

    else:  # 用户名不存在
        user_id = crud.create_user(db=db, username=username, password=password)
        data = schemas.UserBase(user_id=user_id)
        return schemas.CustomResponse(code=200, message="成功创建用户", data=data)


# 登录接口
@user_router.post("/user")
async def user_login(username: str, password: str, db: Session = Depends(get_db)):
    if not crud.username_has_exist(db, username):  # 用户名不存在
        data = None
        return schemas.CustomResponse(code=400, message="用户名不存在", data=data)

    elif crud.check_password(db, username, password):  # 密码正确
        user_id = crud.get_user_id(db, username)
        data = schemas.UserBase(user_id=user_id)
        return schemas.CustomResponse(code=400, message="成功登录", data=data)

    else:  # 密码错误
        return schemas.CustomResponse(code=400, message="成功登录", data=data)

