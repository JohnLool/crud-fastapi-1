import asyncio
from datetime import datetime, timedelta, timezone
from typing import List, Annotated
from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.admin import setup_admin
from app.auth import create_access_token, get_current_user
from app.utils import verify_password
from app.database import get_all_posts, get_post, create_db, get_user, get_all_users, \
    create_user, create_post, update_user, update_post, delete_user, delete_post, get_user_by_username
from app.schemas import Token, UserCreate, UserGet, PostGet, PostCreate, UserUpdate, PostCreate, PostUpdate, PostBase
from app.config import settings


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

setup_admin(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/users/me", response_model=UserGet)
async def read_current_user(current_user: Annotated[UserGet, Depends(get_current_user)]):
    return current_user


@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.post("/auth/", response_model=UserGet)
async def authenticate_user(username: str, password: str):
    user = await get_user_by_username(username)
    if user is None or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return user


@app.post("/users/", response_model=UserCreate)
async def add_user(user: UserCreate):
    if await get_user_by_username(user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    await create_user(user)
    return user


@app.post("/posts/", response_model=PostCreate)
async def add_post(post: PostBase, current_user: UserGet = Depends(get_current_user)):
    post_with_user = PostCreate(**post.dict(), user_id=current_user.id)
    await create_post(post_with_user)
    return post_with_user


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
async def update_user_by_id(user_id: int, user_data: UserUpdate):
    updated_user = await update_user(user_id, user_data)
    return updated_user


@app.put("/users/", response_model=UserGet)
async def update_current_user(user_data: UserUpdate, current_user: UserGet = Depends(get_current_user)):
    updated_user = await update_user(current_user.id, user_data)
    return updated_user


@app.put("/posts/{post_id}", response_model=PostGet)
async def update_post_by_id(post_id: int, post_data: PostUpdate):
    updated_post = await update_post(post_id, post_data)
    return updated_post


@app.put("/posts/{post_id}", response_model=PostGet)
async def update_current_user_post(post_id: int, post_data: PostUpdate, current_user: UserGet = Depends(get_current_user)):
    post = await get_post(post_id)
    if post.user_id == current_user.id:
        updated_post = await update_post(post_id, post_data)
        return updated_post
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")


@app.delete("/users/{user_id}", response_model=UserGet)
async def delete_user_by_id(user_id: int):
    deleted_user = await delete_user(user_id)
    return deleted_user


@app.delete("/users/", response_model=UserGet)
async def delete_current_user(current_user: UserGet = Depends(get_current_user)):
    deleted_user = await delete_user(current_user.id)
    return deleted_user



@app.delete("/posts/{post_id}", response_model=PostGet)
async def delete_post_by_id(post_id: int):
    deleted_post = await delete_post(post_id)
    return deleted_post



@app.delete("/posts/{post_id}", response_model=PostGet)
async def delete_current_user_post(post_id: int, current_user: UserGet = Depends(get_current_user)):
    post = await get_post(post_id)
    if post.user_id == current_user.id:
        deleted_post = await delete_post(post_id)
        return deleted_post
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")


async def main():
    await create_db()


if __name__ == "__main__":
    asyncio.run(main())



