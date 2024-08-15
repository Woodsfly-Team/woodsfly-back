from sqlalchemy import create_engine
 
host = "127.0.0.1:3306"
user = "root"
password = "123456"
database = "Woodsfly"
 
mysql_engine = create_engine("mysql+pymysql://{user}:{password}@{host}/{database}")
result = mysql_engine.execute('select * from mytable')

# 输出查询结果
for row in result:
    print(row)
