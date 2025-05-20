import uuid
from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, Field, EmailStr


class UserBaseSchema(BaseModel):
    id: Optional[uuid.UUID] = Field(default=False)
    username: Optional[str] = Field(default=None)
    email: EmailStr
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    about: Optional[str] = Field(default=None)
    avatar: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)
    birth_date: Optional[datetime] = Field(default=None)
    address: Optional[Union[dict, int]] = Field(default=False)
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)
    is_activate: Optional[bool] = Field(default=False)
    is_locked: Optional[bool] = Field(default=False)

    class Config:
        from_attributes = True


class UserUpdateSchema(BaseModel):
    # username: Optional[str] = Field(default=None)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    about: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)
    birth_date: Optional[datetime] = Field(default=None)


class UserUpdateAvatar(BaseModel):
    avatar: str


class UserChangePasswrdSchema(BaseModel):
    """
    Schema for changing a user's password.

    Attributes:
        current_password (str): The user's current password (min 6 characters).
        new_password (str): The new password the user wants to set (min 6 characters).
    """
    current_password: str = Field(min_length=6)
    new_password: str = Field(min_length=6)