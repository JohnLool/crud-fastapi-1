import asyncio
from typing import List, Annotated
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_all_posts, get_post_by_id, create_db, session_factory, get_user_by_id, get_all_users, \
    insert_user, insert_post, update_user, update_post
from app.schemas import UserCreate, UserGet, PostGet, PostCreate, UserUpdate, PostCreate, PostUpdate

app = FastAPI()


@app.post("/users/", response_model=UserCreate)
async def add_user(user: Annotated[UserCreate, Depends()]):
    await insert_user(user)
    return user


@app.post("/posts/", response_model=PostCreate)
async def add_post(post: Annotated[PostCreate, Depends()]):
    await insert_post(post)
    return post


@app.get("/users/", response_model=List[UserGet])
async def get_users():
    users = await get_all_users()
    return users


@app.get("/users/{user_id}", response_model=UserGet)
async def get_user(user_id: int):
    user = await get_user_by_id(user_id)
    return user


@app.get("/posts/", response_model=List[PostGet])
async def get_posts():
    posts = await get_all_posts()
    return posts


@app.get("/posts/{post_id}", response_model=PostGet)
async def get_post(post_id: int):
    post = await get_post_by_id(post_id)
    return post


@app.put("/users/{user_id}", response_model=UserGet)
async def update_user_by_id(user_id: int, user_data: Annotated[UserUpdate, Depends()]):
    updated_user = await update_user(user_id, user_data)
    return updated_user


@app.put("/posts/{post_id}", response_model=PostGet)
async def update_post_by_id(post_id: int, post_data: Annotated[PostUpdate, Depends()]):
    updated_post = await update_post(post_id, post_data)
    return updated_post


async def main():
    await create_db()


if __name__ == "__main__":
    asyncio.run(main())

