from sqlalchemy import Column, Integer, String, TIMESTAMP,Text
from sqlalchemy.sql import func
#1.用Base类来创建 SQLAlchemy 模型
from database import Base
 
# class User(Base):
#     __tablename__ = "users"
#     #2.创建模型属性/列
#     id = Column(Integer, primary_key=True, index=True)
#     phone = Column(String(50), unique=True, index=True)
#     hashed_password = Column(String(50))
#     is_active = Column(Boolean, default=True)
#     #3.创建关系
#     items = relationship("Item", back_populates="owner")
 
# class Item(Base):
#     __tablename__ = "items"
 
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(50), index=True)
#     description = Column(String(50), index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))
 
#     owner = relationship("User", back_populates="items")

class User(Base):# 用户表
    __tablename__ = "user"
    #2.创建模型属性/列
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50))
    password = Column(String(50))
    avatar = Column(String(100))

class Bird(Base):# 鸟类表
    __tablename__ = "bird"
    #2.创建模型属性/列
    id = Column(Integer, primary_key=True, index=True)
    chinese_name = Column(String(50))
    english_name = Column(String(50))
    bird_order = Column(String(50))
    bird_family = Column(String(50))
    bird_genus = Column(String(50))
    protection_level = Column(String(50))
    introduction = Column(String(500))
    baidu_link = Column(String(100))
    distrbution = Column(String(100))
    image_link = Column(Text)

class Browse(Base):# 浏览记录表
    __tablename__ = "browse"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    bird_id = Column(Integer)
    time = Column(TIMESTAMP(6),server_default=func.current_timestamp(6))

class Star(Base):# 收藏表
    __tablename__ = "star"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    bird_id = Column(Integer)
    time = Column(TIMESTAMP(6),server_default=func.current_timestamp(6))

