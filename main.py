# 程序入口文件。

from fastapi import FastAPI
from fastapi_mail import FastMail, MessageSchema, MessageType
from fastapi import Depends
from dependencies import get_mail
from routers.auth_router import router as auth_router
from routers.name_router import router as name_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(name_router)

@app.get("/mail/test")
async def mail_test(
    email: str,
    mail: FastMail = Depends(get_mail)
):
    message = MessageSchema(
        subject="Test Email",
        recipients=[email],
        body="This is a test email from FastAPI.",
        subtype=MessageType.plain
    )
    await mail.send_message(message)
    return {"message": "邮件发送成功！"}