from typing import List, Union,Any
 
from pydantic import BaseModel



class CustomResponse(BaseModel): # 通用响应体
    code: int
    message: str
    data: Any
 
class UserBase(BaseModel):
    user_id: int

class StarBase(BaseModel): #收藏
    star_id: int

class BrowseBase(BaseModel):
    browse_id: int









class Define(BaseModel): #生物学定义
    bird_order: Union[str, None] = None
    bird_family:Union[str, None] = None
    bird_genus: Union[str, None] = None

class Response_Search_Bird(BaseModel): #查询鸟类响应体
    bird_id: Union[int, None] = None
    chinese_name: Union[str, None] = None
    english_name: Union[str, None] = None
    incidence: Union[str, None] = None
    image: Union[int, None] = None
    define: Define
    habitat: Union[str, None] = None
    introduction: Union[str, None] = None
    level: Union[str, None] = None
    link: Union[str, None] = None

class Response_Matchinfo(BaseModel): #匹配信息响应体
    bird_id: Union[int, None] = None
    chinese_name: Union[str, None] = None
    english_name: Union[str, None] = None
    define: Define



# #1.创建一个 ItemBase 和 UserBase 的 Pydantic模型（或者我们说“schema”）
# class ItemBase(BaseModel):
#     title: str
#     description: Union[str, None] = None
 
# #2.ItemCreate 继承自 ItemBase，他们在创建或读取数据时具有共同的属性。
# class ItemCreate(ItemBase):
#     pass
 
# #3.Item 继承自 ItemCreate，增加 id 和 owner_id 字段
# class Item(ItemCreate):
#     id: int
#     owner_id: int
 
#     class Config:
#         orm_mode = True #使其包含关系字段
 
# class UserBase(BaseModel):
#     phone: str
 
# #为了安全起见，password 不会出现在其他同类 Pydantic模型中，例如用户请求时不应该从 API 返回响应中包含它。
# class UserCreate(UserBase): #字段名对不上会报错，所以单独搞个
#     password: str
 
# class User(UserBase):
#     id: int
#     is_active: bool
#     items: List[Item] = []
 
#     class Config:
#         orm_mode = True