import asyncio
from typing import List, Annotated
from fastapi import FastAPI, Depends

from app.database import create_db, insert_user, insert_post
from app.schemas import UserCreate, PostCreate, UserUpdate, PostCreate

app = FastAPI()


@app.post("/users/", response_model=UserCreate)
async def add_user(user: Annotated[UserCreate, Depends()]):
    await insert_user(user)
    return user

@app.post("/posts/", response_model=PostCreate)
async def add_post(post: Annotated[PostCreate, Depends()]):
    await insert_post(post)
    return post
#
# @app.get("/users/", response_model=List[UserBase])
# async def get_users():
#     return db

async def main():
    await create_db()


if __name__ == "__main__":
    asyncio.run(main())

