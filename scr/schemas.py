from datetime import datetime
from typing import List, Optional, Union

from fastapi import UploadFile
from pydantic import BaseModel, EmailStr, Field


class TagModel(BaseModel):
    name: str = Field(max_length=25)


class TagResponse(TagModel):
    id: int

    class Config:
        from_attributes = True


class NoteBase(BaseModel):
    title: str = Field(max_length=50)
    description: str = Field(max_length=150)


class NoteModel(NoteBase):
    tags: List[int]


class NoteUpdate(NoteModel):
    done: bool


class NoteStatusUpdate(BaseModel):
    done: bool


class NoteResponse(NoteBase):
    id: int
    created_at: datetime
    tags: List[TagResponse]

    class Config:
        from_attributes = True

class CommentBase(BaseModel):
    comment: str = Field(min_length=1, max_length=255)


class CommentResponse(CommentBase):
    id: int
    image_id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        from_attributes = True

class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"

class User(BaseModel):
    user: int

class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RequestEmail(BaseModel):
    email: EmailStr

class PostCreate(BaseModel):
    """
    Створення посту
    """
    text: str
    user: int
    img: UploadFile
    description: str

    class ConfigDict:
        from_attributes = True


class PostBase(BaseModel):
    """
    Схема опублікування
    """
    img: str
    text: str
    user: int
    # img: str = Field(..., title="Світлина")
    # text: str = Field(..., title="Текст")
    # tags: Optional[List[str]] = None
    # user: Optional[int] = None


    class ConfigDict:
        from_attributes = True


class PostList(PostBase):
    """
    Публікації в списку
    """

    pub_date: datetime = Field(..., title="Дата публикации")

    class ConfigDict:
        from_attributes = True


class PostBaseCreateUpdate(PostBase):
    """
    Схема створення/редагування посту
    """
    user: Union[User, int]

class PostCreate(PostBaseCreateUpdate):
    """
    Створення посту
    """
    user: int


class PostUpdate(PostBaseCreateUpdate):
    """
    Редагування посту
    """


class PostSingle(PostBase):
    img: str
    text: str
    user: str
    id: int
    owner_id: int
    url_original: str
    tags: List[str]
    description: Optional[str]
    pub_date: datetime

    class ConfigDict:
        from_attributes = True

