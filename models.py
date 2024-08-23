from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP,VARCHAR
from sqlalchemy.orm import relationship
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

class User(Base):
    __tablename__ = "user"
    #2.创建模型属性/列
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50))
    password = Column(String(50))
    avatar = Column(String(100))

class Bird(Base):
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
    image_link = Column(String(100))

class Browse(Base):
    __tablename__ = "browse"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    bird_id = Column(Integer)
    browse_time = Column(TIMESTAMP(6))

class Collect(Base):
    __tablename__ = "collect"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    bird_id = Column(Integer)
    collect_time = Column(TIMESTAMP(6))

