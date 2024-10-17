import asyncio
from typing import List, Annotated
from fastapi import FastAPI, Depends

from database import create_db, insert_in_db
from schemas import UserCreate, UserBase, UserUpdate
app = FastAPI()


# @app.post("/users/", response_model=UserCreate)
# async def add_user(user: Annotated[UserCreate, Depends()]):
#     db.append(user)
#     return user
#
# @app.get("/users/", response_model=List[UserBase])
# async def get_users():
#     return db

async def main():
    await create_db()
    await insert_in_db()

if __name__ == "__main__":
    asyncio.run(main())

