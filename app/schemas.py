from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserGet(UserBase):
    id: int


class UserUpdate(UserCreate):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class PostBase(BaseModel):
    title: str
    description: str


class PostCreate(PostBase):
    user_id: int


class PostGet(PostCreate):
    id: int


class PostUpdate(PostBase):
    title: str | None = None
    description: str | None = None