from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from models import UserOrm, Base, PostOrm
from config import settings
from schemas import UserCreate, PostCreate, UserUpdate, PostUpdate

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


async def get_user(user_id: int):
    async with session_factory() as session:
        result = await session.execute(select(UserOrm).filter(UserOrm.id == user_id))
        return result.scalar_one_or_none()


async def get_all_posts():
    async with session_factory() as session:
        result = await session.execute(select(PostOrm))
        return result.scalars().all()


async def get_post(post_id: int):
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


async def update_user(user_id: int, user_data: UserUpdate):
    async with session_factory() as session:
        user = await session.get(UserOrm, user_id)
        user.username = user_data.username or user.username
        user.email = user_data.email or user.email
        user.password = user_data.password or user.password
        await session.commit()
        await session.refresh(user)
        return user


async def insert_post(post: PostCreate):
    post_to_add = PostOrm(
        title=post.title,
        description=post.description,
        user_id=post.user_id
    )
    async with session_factory() as session:
        session.add(post_to_add)
        await session.commit()


async def update_post(post_id: int, post_data: PostUpdate):
    async with session_factory() as session:
        post = await session.get(PostOrm, post_id)
        post.title = post_data.title or post.title
        post.description = post_data.description or post.description
        await session.commit()
        await session.refresh(post)
        return post


async def delete_user(user_id: int):
    async with session_factory() as session:
        user = await session.get(UserOrm, user_id)
        await session.delete(user)
        await session.commit()
        return user


async def delete_post(post_id: int):
    async with session_factory() as session:
        post = await session.get(PostOrm, post_id)
        await session.delete(post)
        await session.commit()
        return post
