from fastapi import APIRouter, Query, Depends
from pydantic import EmailStr
from typing import Annotated
from dependencies import get_mail, get_session
from fastapi_mail import FastMail, MessageSchema, MessageType
from models import AsyncSession
import string
import random
from repository.user_repo import EmailCodeRepository
from schemas import ResponseOut

router = APIRouter(prefix="/auth", tags=["用户相关接口"])

@router.get("/code")
async def get_email_code(
    email: Annotated[EmailStr, Query(description="邮箱地址")],
    mail: FastMail = Depends(get_mail),
    session: AsyncSession = Depends(get_session)
):
    # 1. 生成四位数字的验证码
    source = string.digits * 4
    code = ''.join(random.sample(source, 4))

    # 2. 创建消息对象
    message = MessageSchema(
        subject="AI-Name 注册验证码",
        recipients=[email],
        body=f"您的验证码为：{code}，有效期为5分钟。",
        subtype=MessageType.plain
    )
    # 3. 发送邮件
    await mail.send_message(message)
    # 4. 将邮箱和验证码存储到数据库中
    email_code_repo = EmailCodeRepository(session)
    await email_code_repo.create(email=email, code=code)
    return ResponseOut()