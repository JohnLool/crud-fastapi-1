import asyncio
from typing import List, Annotated
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_all_posts, get_post_by_id, create_db,session_factory, get_user_by_id, get_all_users, insert_user, insert_post
from app.schemas import UserCreate, UserGet, PostGet, PostCreate, UserUpdate, PostCreate

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


@app.get("/post/{post_id}", response_model=PostGet)
async def get_post(post_id: int):
    post = await get_post_by_id(post_id)
    return post

async def main():
    await create_db()


if __name__ == "__main__":
    asyncio.run(main())

