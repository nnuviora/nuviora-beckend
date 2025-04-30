import uuid
from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, Field, EmailStr


class UserBaseSchema(BaseModel):
    id: Optional[uuid.UUID] = Field(default=False)
    usename: Optional[str] = Field(default=None)
    email: EmailStr
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
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
    username: Optional[str] = Field(default=None)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)
    birth_date: Optional[datetime] = Field(default=None)
