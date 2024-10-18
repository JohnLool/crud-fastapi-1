import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import URL, create_engine, text, insert

from app.models import UserOrm, Base, PostOrm
from app.config import settings
from app.schemas import UserCreate, PostCreate

engine = create_async_engine(
    url=settings.database_url,
    echo = True
)


session_factory = async_sessionmaker(engine)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def insert_user(user: UserCreate):
    user_to_add = UserOrm(
        username=user.username,
        email=user.email,
        password=user.password
    )
    async with session_factory() as session:
        session.add(user_to_add)
        await session.commit()


async def insert_post(post: PostCreate):
    post_to_add = PostOrm(
        title=post.title,
        description=post.description,
        user_id=post.user_id
    )
    async with session_factory() as session:
        session.add(post_to_add)
        await session.commit()