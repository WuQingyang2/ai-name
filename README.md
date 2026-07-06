# AI Name

一个基于 FastAPI + LangChain 的后端练习项目。

## 环境准备

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 数据库迁移

```bash
alembic upgrade head
```

如果修改了模型，可以生成新的迁移文件：

```bash
alembic revision --autogenerate -m "describe changes"
```

## 运行

```bash
uvicorn main:app --reload
```

接口文档：

```text
http://127.0.0.1:8000/docs
```

## 当前接口

- `GET /mail/test?email=xxx@example.com`：发送测试邮件
- `GET /auth/code?email=xxx@example.com`：发送注册验证码并保存到数据库
