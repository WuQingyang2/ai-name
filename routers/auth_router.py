from fastapi import APIRouter, Query, Depends, HTTPException
from pydantic import EmailStr
from typing import Annotated
from dependencies import get_mail, get_session
from fastapi_mail import FastMail, MessageSchema, MessageType
from models import AsyncSession
import string
import random
from repository.user_repo import EmailCodeRepository, UserRepository
from schemas import ResponseOut
from schemas.user_schemas import RegisterIn, UserCreateSchema, LoginIn, LoginOut
from core.auth import AuthHandler
from models.user import User

router = APIRouter(prefix="/auth", tags=["用户相关接口"])

auth_handler = AuthHandler()

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

@router.post('/register', response_model=ResponseOut)
async def register(
    data: RegisterIn, 
    session: AsyncSession = Depends(get_session)
    ):
    # 1. 检查邮箱是否已经存在
    user_repo = UserRepository(session)
    if await user_repo.email_is_exist(str(data.email)):
        raise HTTPException(status_code=400, detail="邮箱已经存在！")
    # 2. 检查邮箱验证码是否正确
    email_code_repo = EmailCodeRepository(session)
    if not await email_code_repo.check_email_code(email=str(data.email), code=data.code):
        raise HTTPException(status_code=400, detail="邮箱验证码错误！")
    # 3. 创建用户
    try:
        await user_repo.create(UserCreateSchema(email=data.email, username=data.username, password=data.password))
    except Exception as e:
        raise HTTPException(status_code=500, detail="注册失败！")
    return ResponseOut()

@router.post('/login', response_model=LoginOut)
async def login(
    data: LoginIn,
    session: AsyncSession = Depends(get_session),
):
    # 1. 创建user_repo对象
    user_repo = UserRepository(session)
    # 2. 根据邮箱查找用户
    user: User | None = await user_repo.get_by_email(str(data.email))
    if not user:
        raise HTTPException(400, detail="该用户不存在！")
    if not user.check_password(data.password):
        raise HTTPException(400, detail="邮箱或密码错误！")
    # 3. 生成JWToken
    tokens = auth_handler.encode_login_token(user.id)
    return {
        "user": user,
        "token": tokens['access_token']
    }