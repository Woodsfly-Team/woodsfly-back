import uvicorn

from typing import List
 
from fastapi import Depends, FastAPI,HTTPException,Response,UploadFile,File
from fastapi.responses import HTMLResponse,FileResponse
from sqlalchemy.orm import Session
 
import crud, models, schemas
from database import SessionLocal, engine

from yolov8_inference import yolov8_inference
from encode_and_decode import encode_image_to_base64,decode_base64_to_image

#预先创建数据表
models.Base.metadata.create_all(bind=engine)
 
app = FastAPI()
 
 
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
     <!DOCTYPE html>
    <html>
        <head>
            <title>FastAPI HTMLResponse Example</title>
        </head>
        <body>
            <h1>Hello, World!</h1>
        </body>
    </html>
    """
    return html_content

app = FastAPI()


@app.post("/image/")
async def get_image(file:UploadFile = File(...)):
    with open(file.filename, "wb") as buffer:
        buffer.write(await file.read())
    return {'ok':'ok'}

@app.get("/audio/")
async def get_audio():
    return FileResponse("516341.wav", media_type="wav")

# 创建用户接口
@app.post("/createuser/")
async def create_user(username:str,password:str,db: Session = Depends(get_db)):
    if username == None or password == None:#参数错误
        custom_response = schemas.CustomResponse(code=400, message="用户名或密码不能为空", data=None)
        return custom_response
    if crud.get_username_exist(db,username) == True:#用户名已存在
        custom_response = schemas.CustomResponse(code=404, message="用户名已存在", data=None)
        return custom_response
    orm_result = crud.create_user(db=db,username=username,password=password ) # 创建用户
    pyd_user = schemas.User(
        avatar=orm_result.avatar,
        user_id=orm_result.id,
        username=orm_result.username
        )
    custom_response = schemas.CustomResponse(code=200, message="成功创建用户", data=pyd_user)
    return custom_response

# 查询接口
@app.post("/searchbird/")
async def search_bird(bird_info: str,tag: int,user_id: int,db: Session = Depends(get_db)):
    if crud.get_user_id_exist(db,user_id) == False:#用户不存在
        custom_response = schemas.CustomResponse(code=404, message="用户不存在", data=None)
        return custom_response
    if bird_info == None or tag not in [0,1,2]:#参数错误
        custom_response = schemas.CustomResponse(code=400, message="参数错误", data=None)
        return custom_response
    
    if tag == 0: #字段搜索
        bird_name = bird_info
    elif tag == 1: #图片搜索
        # bird_info = encode_image_to_base64('maque.png')
        image_path = decode_base64_to_image(bird_info,user_id)
        bird_name = yolov8_inference(image_path)
        print(bird_name)
    elif tag == 2:  #录音搜索
        bird_name = bird_info
        
    orm_result = crud.search_bird(db,bird_name)
    if orm_result == []:#找不到
        custom_response = schemas.CustomResponse(code=404, message="未找到鸟类", data=None)
        return custom_response
    crud.create_browse(db,user_id,orm_result.id) # 创建浏览记录
    pyd_result = schemas.Response_Search_Bird(
        chinese_name=orm_result.chinese_name,
        define=schemas.Define(bird_family=orm_result.bird_family,bird_genus=orm_result.bird_genus,bird_order=orm_result.bird_order),
        english_name=orm_result.english_name,
        habitat=orm_result.distrbution,
        image=orm_result.image_link,
        link=orm_result.baidu_link,
        introduction=orm_result.introduction,
        level=orm_result.protection_level
        ) 
    custom_response = schemas.CustomResponse(code=200, message="成功", data=pyd_result)
    return custom_response

# 搜索匹配接口 
@app.post("/matchinfo/")
async def search_bird(bird_info: str,db: Session = Depends(get_db)):
    if bird_info == None:#参数错误
        custom_response = schemas.CustomResponse(code=400, message="参数错误", data=None)
        return custom_response
    orm_results = crud.search_birds(db,bird_info)
    if orm_results == []:#找不到
        custom_response = schemas.CustomResponse(code=404, message="未找到鸟类", data=None)
        return custom_response
    pyd_results = [schemas.Response_Matchinfo(
        chinese_name=orm_result.chinese_name,
        english_name=orm_result.english_name,
        define=schemas.Define(bird_family=orm_result.bird_family,bird_genus=orm_result.bird_genus,bird_order=orm_result.bird_order)
    ) for orm_result in orm_results]
    custom_response = schemas.CustomResponse(code=200, message="成功", data=pyd_results)
    return custom_response

# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, phone=user.phone)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)
 
 
# @app.get("/users/", response_model=List[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users
 
 
# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_id(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
 
 
# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)
 
 
# @app.get("/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
 
 
# @app.put("/update_item/{item_id}/")
# def update_item(item_id: int,desc: str, db: Session = Depends(get_db)):
#     db_item = crud.update_item_desc_by_id(db, id=item_id, desc=desc)
#     return db_item
 
 
# @app.delete("/delete_item/{owner_id}/")
# def delete_item(owner_id: int, db: Session = Depends(get_db)):
#     result = crud.delete_item_by_ownerId2(db, owner_id=owner_id)
#     return result
 
 
