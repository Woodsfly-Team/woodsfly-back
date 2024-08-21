from fastapi import FastAPI

# 创建一个 FastAPI 应用实例
app = FastAPI()

# 定义一个字典来模拟用户数据
fake_users_db = {
    "john_doe": {
        "id": "1",
        "name": "John Doe",
        "email": "john@example.com"
    },
    "jane_doe": {
        "id": "2",
        "name": "Jane Doe",
        "email": "jane@example.com"
    }
}

# 定义一个路径操作装饰器
@app.get("/users/{username}")
async def read_user(username: str):
    if username in fake_users_db:
        return fake_users_db[username]
    else:
        return {"error": "User not found"}
# 定义一个路径操作装饰器
@app.get("/")
async def test():

    return {"woodsfly": "server is running"}
