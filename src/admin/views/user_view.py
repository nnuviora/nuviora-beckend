from sqladmin import ModelView
from models.user_model import UserModel


class UserView(ModelView, model=UserModel):
    column_list = [
        "id",
        "username"
    ]