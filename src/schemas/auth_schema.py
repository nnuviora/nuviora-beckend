import uuid
from typing import Union

from pydantic import BaseModel, EmailStr


class LoginSchema(BaseModel):
    login: str
    password: str


class TokenSchema(BaseModel):
    access_token: str


class ForgotPassword(BaseModel):
    hash_password: str
    repeat_password: str


class ChangePassword(ForgotPassword):
    id: Union[uuid.UUID, str]


class RegisterSchema(ForgotPassword):
    email: EmailStr


class ChechEmailSchema(BaseModel):
    email: EmailStr
