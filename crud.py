from sqlalchemy.orm import Session
 
import models, schemas
 
#搜素鸟类
def search_bird(db: Session, bird_info: str):
    orm_result = db.query(models.Bird).filter(models.Bird.chinese_name == bird_info).first()
    if orm_result:
        return orm_result
    return []

def search_birds(db: Session, bird_info: str):
    attributes = ['chinese_name', 'english_name', 'bird_order','bird_family', 'bird_genus']
    for attr in attributes:
        orm_results = db.query(models.Bird).filter(getattr(models.Bird, attr).like(f'%{bird_info}%')).all()
        if orm_results:
            return orm_results
    return []

# #通过 ID 查询单个用户。
# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()
 
# #通过电子邮件查询单个用户。
# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()
 
# #查询多个用户
# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()
 
# #查询多个项目
# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()

# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
 
# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item

# def update_item_desc_by_id(db: Session, id: int, desc: str):
#     db_item = db.query(models.Item).filter_by(id=id).first()
#     db_item.description = desc
#     db.commit()
#     db.refresh(db_item)
#     return db_item

# # 批量删除1
# def delete_item_by_ownerId1(db: Session, owner_id: int):
#     db.query(models.Item).filter_by(owner_id=owner_id).delete(synchronize_session=False)
#     db.commit()
#     return True
 
# # 批量删除2
# def delete_item_by_ownerId2(db: Session, owner_id: int):
#     db_items = db.query(models.Item).filter_by(owner_id=owner_id).all()
#     [db.delete(item) for item in db_items]
#     db.commit()
#     return True

