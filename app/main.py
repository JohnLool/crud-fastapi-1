import asyncio
from typing import List, Annotated
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.database import get_all_posts, get_post, create_db, get_user, get_all_users, \
    insert_user, insert_post, update_user, update_post, delete_user, delete_post
from app.schemas import UserCreate, UserGet, PostGet, PostCreate, UserUpdate, PostCreate, PostUpdate

app = FastAPI()

origins = [
    "http://localhost:63342",
    "http://127.0.0.1:63342"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
async def get_user_by_id(user_id: int):
    user = await get_user(user_id)
    return user


@app.get("/posts/", response_model=List[PostGet])
async def get_posts():
    posts = await get_all_posts()
    return posts


@app.get("/posts/{post_id}", response_model=PostGet)
async def get_post_by_id(post_id: int):
    post = await get_post(post_id)
    return post


@app.put("/users/{user_id}", response_model=UserGet)
async def update_user_by_id(user_id: int, user_data: Annotated[UserUpdate, Depends()]):
    updated_user = await update_user(user_id, user_data)
    return updated_user


@app.put("/posts/{post_id}", response_model=PostGet)
async def update_post_by_id(post_id: int, post_data: Annotated[PostUpdate, Depends()]):
    updated_post = await update_post(post_id, post_data)
    return updated_post


@app.delete("/users/{user_id}", response_model=UserGet)
async def delete_user_by_id(user_id: int):
    deleted_user = await delete_user(user_id)
    return deleted_user


@app.delete("/posts/{post_id}", response_model=PostGet)
async def delete_post_by_id(post_id: int):
    deleted_post = await delete_post(post_id)
    return deleted_post


async def main():
    await create_db()


if __name__ == "__main__":
    asyncio.run(main())

