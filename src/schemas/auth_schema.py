import uuid
import re
from typing import Union, Optional

from pydantic import BaseModel, EmailStr, field_validator, Field

from .user_schema import UserBaseSchema


class LoginSchema(BaseModel):
    email: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    user: Optional[UserBaseSchema] = Field(default=None)


class ForgotPassword(BaseModel):
    hash_password: str
    repeat_password: str

    @field_validator("hash_password")
    def check_string(cls, v):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z]).{6,}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid password")
        return v


class ChangePassword(ForgotPassword):
    id: Union[uuid.UUID, str]


class RegisterSchema(ForgotPassword):
    email: EmailStr


class ChechEmailSchema(BaseModel):
    email: EmailStr
