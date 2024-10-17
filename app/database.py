import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import URL, create_engine, text, insert

from app.models import User, Base
from config import settings


engine = create_async_engine(
    url=settings.database_url,
    echo = True
)


session_factory = async_sessionmaker(engine)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def insert_in_db():
    user_test = User(username="user", email='user@gmail.com', password="qwerty123")
    async with session_factory() as session:
        session.add(user_test)
        await session.commit()
