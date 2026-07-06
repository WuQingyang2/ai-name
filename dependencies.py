# FastAPI项目的依赖项。

from core.mail import create_mail_instance
from fastapi_mail import FastMail

from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator
from models import AsyncSessionFactory

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session = AsyncSessionFactory()
    try:
        yield session
    finally:
        await session.close()

async def get_mail() -> FastMail:
    return create_mail_instance()