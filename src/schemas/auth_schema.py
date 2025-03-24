from pydantic import BaseModel, EmailStr


class LoginSchema(BaseModel):
    login: str
    password: str


class TokenSchema(BaseModel):
    access_token: str


class RegisterSchema(BaseModel):
    username: str
    email: EmailStr
    hash_password: str
