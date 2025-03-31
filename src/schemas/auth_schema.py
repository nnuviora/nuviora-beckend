import uuid
import re
from typing import Union

from pydantic import BaseModel, EmailStr, field_validator


class LoginSchema(BaseModel):
    email: str
    password: str


class TokenSchema(BaseModel):
    access_token: str


class ForgotPassword(BaseModel):
    hash_password: str
    repeat_password: str

    @field_validator("hash_password")
    def check_string(cls, v):
        pattern = r"^(?=(.*\d){6,})(?=(.*[a-z]){1,})(?=(.*[A-Z]){1,}).*$"
        if not re.match(pattern, v):
            raise ValueError("Invalid password")
        return v


class ChangePassword(ForgotPassword):
    id: Union[uuid.UUID, str]


class RegisterSchema(ForgotPassword):
    email: EmailStr


class ChechEmailSchema(BaseModel):
    email: EmailStr
