from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserGet(UserBase):
    id: int


class UserUpdate(UserBase):
    password: str = None


class PostCreate(BaseModel):
    user_id: int
    title: str
    description: str


class PostGet(PostCreate):
    id: int


class PostUpdate(PostCreate):
    title: str | None
    description: str | None