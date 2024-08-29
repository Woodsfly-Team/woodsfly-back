# 引入音频识别模型相关库文件
from BirdClass.infer import infer

# 引入FastAPI相关库文件
from fastapi import Depends, FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

# 引入数据库相关库文件
import crud
import schemas
from database import get_db

# 引入yolov8相关库文件
from yolov8.yolov8_inference import yolov8_inference
from datetime import datetime
import os
from random_image import get_random_image_from_folder

# 引入接口
import user_routers
import website_routers

# 配置FastAPI实例
app = FastAPI()

# 引入接口
app.include_router(user_routers.user_router)
app.include_router(website_routers.website_router)


# 测试启动接口
@app.get("/is-running")
async def is_running():
    return "server is running"


# 测试接口
@app.get("/test")
async def get_star_status(user_id=1, bird_id=1, db: Session = Depends(get_db)):
    try:
        data = crud.get_star_status(db=db, user_id=user_id, bird_id=bird_id)
        return schemas.CustomResponse(code=200, message="存在记录", data=data)
    except Exception as e:
        data = None
        return schemas.CustomResponse(code=404, message=e, data=data)





# 图片接口
@app.post("/image")
async def get_image(file_id: int, db: Session = Depends(get_db)):
    brid_name = crud.search_bird_by_id(db,file_id).english_name
    print(brid_name)
    if brid_name is None:#找不到
        return schemas.CustomResponse(code=404, message="未找到鸟类", data=None)
    
    folder_path = f'datasets/{brid_name}'
    file_path = get_random_image_from_folder(folder_path)
    return FileResponse(path=file_path)


# 音频接口
@app.get("/audio/")
async def get_audio():
    return FileResponse("user_data/516341.wav", media_type="wav")

# 预测接口
@app.post("/predict")
async def predict(user_id: int,tag: int,file: UploadFile = File(...),db: Session = Depends(get_db)):
    if crud.get_user_id_exist(db,user_id) is False:#用户不存在
        data = None
        return schemas.CustomResponse(code=404, message="用户不存在", data=data)
    
    if file is None or tag not in [1,2]:#参数错误
        data = None
        return schemas.CustomResponse(code=400, message="参数错误", data=data)
    
    content_type = file.content_type
    if (
        tag == 1
        and content_type == "image/png"
        or content_type == "image/jpeg"
        or content_type == "image/jpg"
    ):
        current_datetime = datetime.now()
        save_path = (
            f"user_data/{user_id}/image/{current_datetime.year}/"
            f"{current_datetime.year}_{current_datetime.month}/{current_datetime.month}_{current_datetime.day}/"
            f"{current_datetime.hour}_{current_datetime.minute}_{current_datetime.second}/"
            f"{user_id}_{file.filename}"
        )

        # 确保输出目录存在
        output_dir = "/".join(save_path.split("/")[:-1])
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            # 保存文件
            with open(save_path, "wb") as buffer:
                buffer.write(await file.read())
            
        bird_name,score = yolov8_inference(save_path)

    elif tag == 2 : # 音频识别
        current_datetime = datetime.now()
        save_path = (
            f"user_data/{user_id}/audio/{current_datetime.year}/"
            f"{current_datetime.year}_{current_datetime.month}/{current_datetime.month}_{current_datetime.day}/"
            f"{current_datetime.hour}_{current_datetime.minute}_{current_datetime.second}/"
            f"{user_id}_{file.filename}"
        )
        # 确保输出目录存在
        output_dir = "/".join(save_path.split("/")[:-1])
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            # 保存文件
            with open(save_path, "wb") as buffer:
                buffer.write(await file.read())

        bird_name, score = infer(audio_path=save_path)

    if bird_name is None:#找不到
        return schemas.CustomResponse(code=404, message="未找到鸟类", data=None)

    orm_result = crud.search_bird(db,bird_name)

    if orm_result is None:#找不到
        return schemas.CustomResponse(code=404, message="未找到鸟类", data=None)

    # crud.create_browse(db,user_id,orm_result.id) # 创建浏览记录

    # 将orm转换成pydantic
    pyd_result = schemas.Response_Search_Bird(
        bird_id = orm_result.id,
        chinese_name = orm_result.chinese_name,
        define=schemas.Define(
            bird_family = orm_result.bird_family,
            bird_genus = orm_result.bird_genus,
            bird_order = orm_result.bird_order
            ),
        english_name = orm_result.english_name,
        habitat = orm_result.distrbution,
        image = orm_result.id,
        link = orm_result.baidu_link,
        introduction = orm_result.introduction,
        level = orm_result.protection_level,
        incidence = "{:.2f}%".format(score*100.0)
        ) 
    return schemas.CustomResponse(code=200, message="成功", data=pyd_result)



# 快速搜索接口
@app.get("/search")
async def search_birds(bird_name: str, db: Session = Depends(get_db)):
    orm_results = crud.search_birds(db, bird_name)
    if orm_results is None:  # 找不到
        return schemas.CustomResponse(code=404, message="未找到鸟类", data=None)
    
    pyd_results = [
        schemas.Response_Matchinfo(
            bird_id=orm_result.id,
            chinese_name=orm_result.chinese_name,
            english_name=orm_result.english_name,
            define=schemas.Define(
                bird_family=orm_result.bird_family,
                bird_genus=orm_result.bird_genus,
                bird_order=orm_result.bird_order,
            ),
        )
        for orm_result in orm_results
    ]
    return schemas.CustomResponse(code=200, message="成功", data=pyd_results)



# 搜索详情接口
@app.post("/search")
async def search_bird(bird_id: int, db: Session = Depends(get_db)):

    orm_result = crud.search_bird_by_id(db, bird_id)
    if orm_result is None:  # 找不到
        return schemas.CustomResponse(code=404, message="未找到鸟类", data=None)
    
    # 将orm转换成pydantic
    pyd_result = schemas.Response_Search_Bird(
        bird_id = orm_result.id,
        chinese_name = orm_result.chinese_name,
        define=schemas.Define(
            bird_family = orm_result.bird_family,
            bird_genus = orm_result.bird_genus,
            bird_order = orm_result.bird_order
            ),
        english_name = orm_result.english_name,
        habitat = orm_result.distrbution,
        image = orm_result.id,
        link = orm_result.baidu_link,
        introduction = orm_result.introduction,
        level = orm_result.protection_level,
        incidence = "---"
        ) 
    return schemas.CustomResponse(code=200, message="成功", data=pyd_result)


@app.get("/star")
async def get_star_status(user_id: int, bird_id: int, db: Session = Depends(get_db)):
    try:
        data = schemas.StarBase(star_id=crud.get_star_status(db, user_id, bird_id))
        return schemas.CustomResponse(code=200, message="成功", data=data)
    except Exception as e:
        data = schemas.StarBase(star_id=0)
        return schemas.CustomResponse(code=404, message=str(e), data=data)


# 查询收藏列表接口
@app.post("/star")
async def get_star_list(user_id: int, db: Session = Depends(get_db)):
    star_list = crud.get_star_list(db, user_id)
    if star_list is None:  # 找不到
        return schemas.CustomResponse(code=200, message="未创建收藏", data=None)
    
    # 根据 browse_time 排序，降序
    star_list_sorted = sorted(star_list, key=lambda x: x.time, reverse=True)
    
    pyd_results = []
    for star in star_list_sorted:
        orm_result = crud.search_bird_by_id(db, star.bird_id)
        pyd_results.append(
            schemas.Response_Star_List(
                star_id = star.id,
                star_time = str(star.time).split('.')[0],
                bird_id = star.bird_id,
                chinese_name = orm_result.chinese_name,
                english_name = orm_result.english_name,
                define=schemas.Define(
                    bird_family = orm_result.bird_family,
                    bird_genus = orm_result.bird_genus,
                    bird_order = orm_result.bird_order,
                )
            )
        )  
        
    return schemas.CustomResponse(code=200, message="成功", data=pyd_results)

# 收藏接口
@app.put("/star")
async def create_star(user_id: int, bird_id: int, db: Session = Depends(get_db)):
    try:
        data = schemas.StarBase(star_id = crud.create_star(db, user_id, bird_id))
        return schemas.CustomResponse(code=200, message="收藏成功", data=data)
    except Exception as e:
        data = schemas.StarBase(star_id=0)
        return schemas.CustomResponse(code=404, message=str(e), data=data)
    
# 取消收藏接口
@app.delete("/star")
async def delete_star(star_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_star(db, star_id)
        return schemas.CustomResponse(code=200, message="取消收藏成功", data=None)
    except Exception as e:
        return schemas.CustomResponse(code=404, message=str(e), data=None)
    
# 查询浏览记录列表接口
@app.post("/browse")
async def get_browse_list(user_id: int, db: Session = Depends(get_db)):
    browse_list = crud.get_browse_list(db, user_id)
    if browse_list is None:  # 找不到
        return schemas.CustomResponse(code=200, message="未创建收藏", data=None)
    
    # 根据 browse_time 排序，降序
    browse_list_sorted = sorted(browse_list, key=lambda x: x.time, reverse=True)
    
    pyd_results = []
    for browse in browse_list_sorted:
        orm_result = crud.search_bird_by_id(db, browse.bird_id)
        pyd_results.append(
            schemas.Response_Browse_List(
                browse_id = browse.id,
                browse_time = str(browse.time).split('.')[0],
                bird_id = browse.bird_id,
                chinese_name = orm_result.chinese_name,
                english_name = orm_result.english_name,
                define=schemas.Define(
                    bird_family = orm_result.bird_family,
                    bird_genus = orm_result.bird_genus,
                    bird_order = orm_result.bird_order,
                )
            )
        )  
        
    return schemas.CustomResponse(code=200, message="成功", data=pyd_results)

# 创建浏览记录接口
@app.put("/browse")
async def create_browse(user_id: int, bird_id: int, db: Session = Depends(get_db)):
    try:
        browse_id_exist = crud.get_browse_status(db, user_id, bird_id)
        if browse_id_exist > 0:
            crud.update_browse_time(db, browse_id_exist)
            data = schemas.BrowseBase(browse_id=browse_id_exist)
            return schemas.CustomResponse(code=200, message="浏览记录更新成功", data=data)
    except Exception as e:
        
        try:
            data = schemas.BrowseBase(browse_id = crud.create_browse(db, user_id, bird_id))
            return schemas.CustomResponse(code=200, message="浏览记录创建成功", data=data)
        except Exception as e:
            data = schemas.BrowseBase(browse_id=0)
            return schemas.CustomResponse(code=404, message=str(e), data=data)
    

# 删除浏览记录接口
@app.delete("/browse")
async def delete_browse(browse_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_browse(db, browse_id)
        return schemas.CustomResponse(code=200, message="浏览记录删除成功", data=None)
    except Exception as e:
        return schemas.CustomResponse(code=404, message=str(e), data=None)


