from sqladmin import ModelView
from models.user_model import (
    UserModel,
    RoleModel,
    TokenModel,
)


class UserView(ModelView, model=UserModel):
    column_list = ["id", "username"]


class RoleView(ModelView, model=RoleModel):
    column_list = ["id", "role"]


class TokenView(ModelView, model=TokenModel):
    column_list = [
        "id",
        "user_id",
        "refresh_token",
        "expires_at",
        "user_agent",
        "created_at",
    ]
