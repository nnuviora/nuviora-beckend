import pickle
import asyncio

import cloudinary
import cloudinary.uploader
from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status,
    Path,
    Query,
    UploadFile,
    File,
)
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession

from scr.database.db import get_db
from scr.database.models import User
from scr.schemas import UserResponse
from scr.services.auth import auth_service
from scr.conf.config import config
from scr.repository import users as repositories_users

router = APIRouter(prefix="/users", tags=["users"])

cloudinary.config(
    cloud_name=config.CLD_NAME,
    api_key=config.CLD_API_KEY,
    api_secret=config.CLD_API_SECRET,
    secure=True,
)


@router.get("/me", response_model=UserResponse, dependencies=[Depends(RateLimiter(times=1, seconds=20))],)
async def get_current_user(user: User = Depends(auth_service.get_current_user)):
    """
    The get_current_user function is a dependency that will be injected into the
        get_current_user endpoint. It uses the auth_service to retrieve the current user,
        and returns it if found.

    :param user: User: Get the current user
    :return: The current user, which is stored in the dependency
    :doc-author: Trelent
    """
    return {"user": user, "detail": "User successfully retrieved"}


@router.patch("/avatar", response_model=UserResponse, dependencies=[Depends(RateLimiter(times=1, seconds=20))],)
async def get_current_user(
    file: UploadFile = File(),
    user_curr: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    The get_current_user function is a dependency that returns the current user.
    It will be used by FastAPI to validate the token and get its associated user.


    :param file: UploadFile: Get the file from the request
    :param user: User: Get the user object from the database
    :param db: AsyncSession: Create a database session
    :param : Get the current user from the database
    :return: The current user, based on the token
    :doc-author: Trelent
    """
    public_id = f"Web09/{user_curr.email}"
    res = cloudinary.uploader.upload(file.file, public_id=public_id, overwrite=True)
    # print(res)
    res_url = cloudinary.CloudinaryImage(public_id).build_url(
        width=250, height=250, crop="fill", version=res.get("version")
    )
    user = await repositories_users.update_avatar_url(user_curr.email, res_url, db)
    auth_service.cache.set(user_curr.email, pickle.dumps(user_curr))
    auth_service.cache.expire(user_curr.email, 300)
    return {"user": user_curr, "detail": "User avatar successfully retrieved"}