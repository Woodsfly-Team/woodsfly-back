#1.导入 SQLAlchemy 部件
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
 
#2.为 SQLAlchemy 定义数据库 URL地址
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://woodsflyDB:77528888@59.110.123.151:3306/woodsflydb?charset=utf8mb4"
 
#3.创建 SQLAlchemy 引擎
engine = create_engine( SQLALCHEMY_DATABASE_URL )
#4.创建一个SessionLocal 数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
#5.创建一个Base类
Base = declarative_base()


# 数据库连接
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 预先创建数据表
Base.metadata.create_all(bind=engine)
