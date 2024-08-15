import pymysql


conn = pymysql.connect(
    host = 'localhost',
    port=3306,
    user='root',
    passwd='123456',
    database='woodsfly_database',
    charset='utf8'
)

cursor = conn.cursor()

sql = 'select * from users'
count = cursor.execute(sql)
print(count)
result = cursor.fetchall()

for i in result:
    print(i)

if conn:
    print("success")
else:
    print("error")