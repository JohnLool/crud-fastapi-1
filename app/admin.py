from fastapi import FastAPI
from sqladmin import Admin, ModelView

from app.database import engine
from app.models import UserOrm, PostOrm


class UserAdmin(ModelView, model=UserOrm):
    column_list = ["id", "username", "email", "is_active", "is_superuser"]

    form_columns = ["username", "email", "hashed_password", "is_active", "is_superuser"]
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"


class PostAdmin(ModelView, model=PostOrm):
    column_list = [PostOrm.id, PostOrm.title, PostOrm.user_id, PostOrm.created_at]
    name = "Post"
    name_plural = "Posts"
    icon = "fa-solid fa-file"


def setup_admin(app: FastAPI):
    admin = Admin(app, engine)
    admin.add_view(UserAdmin)
    admin.add_view(PostAdmin)
