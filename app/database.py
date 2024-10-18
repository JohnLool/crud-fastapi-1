from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

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


async def get_all_users():
    async with session_factory() as session:
        result = await session.execute(select(UserOrm))
        return result.scalars().all()


async def get_user_by_id(user_id: int):
    async with session_factory() as session:
        result = await session.execute(select(UserOrm).filter(UserOrm.id == user_id))
        return result.scalar_one_or_none()


async def get_all_posts():
    async with session_factory() as session:
        result = await session.execute(select(PostOrm))
        return result.scalars().all()


async def get_post_by_id(post_id: int):
    async with session_factory() as session:
        result = await session.execute(select(PostOrm).filter(PostOrm.id == post_id))
        return result.scalar_one_or_none()


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