from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from fastapi import HTTPException, status

from app.models import UserOrm, Base, PostOrm
from app.config import settings
from app.schemas import UserCreate, PostCreate, UserUpdate, PostUpdate
from app.auth import hash_password, verify_password


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
        user = await session.get(UserOrm, user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User not found")
        return user


async def get_user_by_username(username: str):
    async with session_factory() as session:
        result = await session.execute(select(UserOrm).filter(UserOrm.username == username))
        return result.scalar_one_or_none()


async def get_all_posts():
    async with session_factory() as session:
        result = await session.execute(select(PostOrm))
        return result.scalars().all()


async def get_post(post_id: int):
    async with session_factory() as session:
        result = await session.execute(select(PostOrm).filter(PostOrm.id == post_id))
        return result.scalar_one_or_none()


async def create_user(user: UserCreate):
    user_to_add = UserOrm(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    async with session_factory() as session:
        session.add(user_to_add)
        await session.commit()


async def update_user(user_id: int, user_data: UserUpdate):
    async with session_factory() as session:
        user = await session.get(UserOrm, user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User not found")
        user.username = user_data.username or user.username
        user.email = user_data.email or user.email
        user.password = user_data.password or user.password
        await session.commit()
        await session.refresh(user)
        return user


async def create_post(post: PostCreate):
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
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with ID: {post_id} not found"
            )
        post.title = post_data.title or post.title
        post.description = post_data.description or post.description
        await session.commit()
        await session.refresh(post)
        return post


async def delete_user(user_id: int):
    async with session_factory() as session:
        user = await session.get(UserOrm, user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found")
        await session.delete(user)
        await session.commit()
        return user


async def delete_post(post_id: int):
    async with session_factory() as session:
        post = await session.get(PostOrm, post_id)
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with ID: {post_id} not found"
            )
        await session.delete(post)
        await session.commit()
        return post
