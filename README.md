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
