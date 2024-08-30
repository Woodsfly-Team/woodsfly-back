# woodsfly-back 

这是鸟林通app的后端代码仓库，基于 Python + FastAPI 开发

仓库地址：https://github.com/Woodsfly-Team/woodsfly-back.git

**感谢你为 woodsfly-back 项目做出贡献！**

## 项目运行要求
- Python 3.11+
- pip

## 启动指南
1. 安装依赖

   我们的依赖已经记录在 `requirements.txt` 文件中，由于在不同平台上所需要的依赖也有所不同，请使用我们提供的如下脚本来安装依赖。

   ```bash
   # 安装依赖

   # 方法一
   python -m ppm.pip -i
   # 方法二
   python -m ppm.pip --install
   ```
2. 启动项目
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```


## 推荐开发工具

- [VsCode](https://code.visualstudio.com/)
- [Ruff 插件](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)

## 项目分支

- `main` 主分支（生产环境）

  用于生产环境的线上版本代码。不允许直接向 `main` 分支提交代码，需要通过 Pull Request 从 `dev` 分支合并代码。（此操作仅由项目管理员完成）

- `dev` 开发分支（测试环境）

  用于测试新功能和最新的 bug 修改。不允许直接向 `dev` 分支提交代码，需要通过 Pull Request 从 其他 分支合并代码。

## 贡献指南

1. 准备新分支

   在本地拉取最新的项目代码/同步到最新的项目代码，切换到 `dev` 分支，新建一个分支 `example`。

   ```bash
   # 同步远端仓库最新进度
   git fetch
   # 切换到 dev 分支
   git checkout dev
   # 拉取最新代码
   git pull
   # 新建分支
   git checkout -b examplebranch
   ```

2. 修改代码并提交新分支

   在自测完成后，请提交代码。**请注意，请你再次确认你的代码已经通过了你的本地测试。**

   ```bash
   # 添加修改
   git add .
   # 提交修改
   git commit -m "message"
   # 推送到远程仓库
   git push origin examplebranch
   ```

   请在提交信息 `message` 处填写你本次对代码修改的内容。

3. 提交 Pull Request

   提交 Pull Request 从 `examplbranch` 到 `main` 分支。在 Pull Request 中，请确保你的代码通过了所有的测试，没有任何冲突。在 Pull Request 中，请详细描述你的修改，以及你的修改如何解决了问题。

   你需要请求一位其他人员来 code review 你的代码。

   然后，code reviewer 将授权你的 Pull Request 请求。

4. 合并 Pull Request

   当你的 Pull Request 被授权后，你可以将你的代码合并到 `main` 分支。在合并之前，请确保你的代码没有任何冲突，也没有任何测试失败。合并完成后，你可以安全地删除分支 `examplebranch`。

   **请注意：严格禁止直接 push 到 `main` 分支**

## 项目代码编写格式规范说明

### 为了确保代码的一致性和可读性，特制定以下代码规范

1. 注释

   功能注释：每个函数或方法前应有注释，描述其功能和输入输出。
   - 示例：
   ```Python
   def authenticate_user(username: str, password: str) -> bool:
    """
    验证用户的用户名和密码是否正确。

    :param username: 用户名
    :param password: 密码
    :return: 如果验证成功返回True，否则返回False
    """
    # 实现逻辑
    pass
   ```
   
   代码注释：复杂逻辑需添加必要的代码行注释，确保他人容易理解。
   - 示例：
   ```Python
   # 使用哈希算法比较密码
   hashed_password = hash(password)
   if hashed_password == stored_hashed_password:
       return True
   else:
       return False
   ```

3. 命名规范

   变量命名：采用小写字母加下划线方式（snake_case）。
   - 示例：
   ```Python
   def fetch_user_details(user_id: int):
    pass
   ```
   
   类命名：采用大写字母开头的驼峰式命名（CamelCase）。
   - 示例：
   ```Python
   class UserAccount:
    pass
   ```
   
   函数命名：同变量命名规则，小写加下划线。

5. 导入管理

   标准库导入：放在最上方。
   
   第三方库导入：紧接在标准库导入之后。
   
   本地模块导入：位于第三方库导入下方，并按逻辑分组。

   - 示例：
   ```Python
   import os
   from datetime import datetime
   
   from fastapi import FastAPI, UploadFile, File
   from fastapi.responses import FileResponse
   from fastapi.staticfiles import StaticFiles
   from sqlalchemy.orm import Session
   
   from . import crud, schemas
   from .database import get_db
   ```

7. 异常处理
   
   捕获特定异常：避免使用except Exception as e，而应该尽量捕获具体的异常类型。
   
   异常信息记录：记录详细的异常信息，便于调试。
   - 示例：
   ```Python
   def process_file(file: UploadFile) -> dict:
    try:
        # 处理文件逻辑
        return {"status": "success"}
    except FileNotFoundError:
        return {"status": "error", "message": "指定文件未找到"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
   ```

9. 接口设计

   RESTful API：遵循RESTful原则设计API，使用恰当的HTTP动词。
   
   返回结构：统一返回结果的结构，如示例中的schemas.CustomResponse。

   - 示例：
   ```Python
   from fastapi import APIRouter
   router = APIRouter()
   
   @router.get("/users/{user_id}", response_model=schemas.User)
   def read_user(user_id: int, db: Session = Depends(get_db)):
       db_user = crud.get_user(db, user_id=user_id)
       if db_user is None:
           raise HTTPException(status_code=404, detail="User not found")
       return db_user
   ```

11. 数据库操作

   会话管理：使用依赖注入管理数据库会话，如db: Session = Depends(get_db)。
   
   事务控制：对于涉及多个操作的业务逻辑，考虑使用事务保证数据一致性。

   - 示例：
   ```Python
   from sqlalchemy.orm import Session
   
   def update_user(db: Session, user_id: int, new_data: schemas.UserUpdate):
       db_user = crud.get_user(db, user_id=user_id)
       if db_user is None:
           raise HTTPException(status_code=404, detail="User not found")
       # 更新用户信息
       pass
   ```

11. 文件上传与处理

   路径构造：动态构造文件保存路径，确保路径合理且安全。
   
   文件保存：检查并创建必要目录后再保存文件。

   - 示例：
   ```Python
   @app.post("/uploadfile/")
   async def create_upload_file(file: UploadFile = File(...)):
       # 构造保存路径
       path = f"uploads/{datetime.now().strftime('%Y%m%d')}/{file.filename}"
       # 保存文件
       with open(path, "wb") as buffer:
           buffer.write(await file.read())
       return {"filename": file.filename}
   ```
