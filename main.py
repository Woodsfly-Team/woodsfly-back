
from BirdClass.macls.predict import MAClsPredictor
from BirdClass.macls.utils.utils import add_arguments, print_arguments



from fastapi import Depends, FastAPI,UploadFile,File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
 
import crud
import models
import schemas
from database import SessionLocal, engine

from yolov8_inference import yolov8_inference
from encode_and_decode import encode_image_to_base64,decode_base64_to_image,encode_audio_to_base64,decode_base64_to_audio

from datetime import datetime
import os

#预先创建数据表
models.Base.metadata.create_all(bind=engine)
 
app = FastAPI()
# 数据库连接
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 静态资源
app.mount("/assets", StaticFiles(directory="2125_artxibition/assets"), name="static")

# 测试接口
@app.get("/is-running")
async def is_running():
    return "server is running"

# 测试接口
@app.get("/test")
async def test():
    lable,_ = infer('BirdClass/configs/resnet_se.yml',False,'user_data/516341.wav','BirdClass/models/ResNetSE_Fbank/best_model/')
    return lable


# 首页接口
@app.get("/")
async def read_index():
    return FileResponse("2125_artxibition/index.html")
# 图片接口
@app.post("/files")
async def get_image():
    # with open(file.filename, "wb") as buffer:
    #     buffer.write(await file.read())
    return FileResponse("D:/HuaweiMoveData/Users/chen/Desktop/440px-Common_hoopoe_-_Upupa_epops_06.jpg")
# 音频接口
@app.get("/audio/")
async def get_audio():
    return FileResponse("516341.wav", media_type="wav")

@app.post("/predict")
async def predict(user_id: int,tag: int,file: UploadFile = File(...),db: Session = Depends(get_db)):
    if crud.get_user_id_exist(db,user_id) == False:#用户不存在
        custom_response = schemas.CustomResponse(code=404, message="用户不存在", data=None)
        return custom_response
    if file == None or tag not in [1,2]:#参数错误
        custom_response = schemas.CustomResponse(code=400, message="参数错误", data=None)
        return custom_response
    
    content_type = file.content_type
    if tag == 1 and content_type == 'image/png' or content_type == 'image/jpeg' or content_type == 'image/jpg':
        current_datetime = datetime.now()
        save_path = f'user_data/{user_id}/image/{current_datetime.year}/' \
                       f'{current_datetime.year}_{current_datetime.month}/{current_datetime.month}_{current_datetime.day}/' \
                       f'{current_datetime.hour}_{current_datetime.minute}_{current_datetime.second}/' \
                       f'{user_id}_{file.filename}'
    
        # 确保输出目录存在
        output_dir = '/'.join(save_path.split('/')[:-1])
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            # 保存文件
            with open(save_path, "wb") as buffer:
                buffer.write(await file.read())
    elif tag == 2 : # 音频识别
        current_datetime = datetime.now()
        save_path = f'user_data/{user_id}/audio/{current_datetime.year}/' \
                       f'{current_datetime.year}_{current_datetime.month}/{current_datetime.month}_{current_datetime.day}/' \
                       f'{current_datetime.hour}_{current_datetime.minute}_{current_datetime.second}/' \
                       f'{user_id}_{file.filename}'
        # 确保输出目录存在
        output_dir = '/'.join(save_path.split('/')[:-1])
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            # 保存文件
            with open(save_path, "wb") as buffer:
                buffer.write(await file.read())

        bird_name,score = infer('BirdClass/configs/resnet_se.yml',False,audio_path=save_path,model_path='BirdClass/models/ResNetSE_Fbank/best_model/')

    if bird_name == None:#找不到
        custom_response = schemas.CustomResponse(code=404, message="未找到鸟类", data=None)
        return custom_response
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
        level=orm_result.protection_level,
        incidence="{:.2f}%".format(score*100.0)
        ) 
    custom_response = schemas.CustomResponse(code=200, message="成功", data=pyd_result)
    return custom_response


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
        bird_name = '戴胜'
        
        
    if bird_name == None:#找不到
        custom_response = schemas.CustomResponse(code=404, message="未找到鸟类", data=None)
        return custom_response
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
        level=orm_result.protection_level,
        incidence="99.2%"
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
 

def infer(configs: str, use_gpu: bool, audio_path: str, model_path: str):
    # 获取识别器
    predictor = MAClsPredictor(configs=configs,
                            model_path=model_path,
                            use_gpu=use_gpu)

    label, score = predictor.predict(audio_data=audio_path)

    print(f'音频：{audio_path} 的预测结果标签为：{label}，得分：{score}')
    return label,score
