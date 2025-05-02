# api/v1/endpoints/avatar.py

from fastapi import UploadFile, File, Depends
import boto3
from botocore.exceptions import BotoCoreError, ClientError
import uuid
import io
from PIL import Image
from fastapi.routing import APIRouter
from fastapi import status, HTTPException
# from api.v1.dependencies import get_current_user, get_load_service, auth_dep, user_dep
from api.v1.dependencies import get_current_user, get_load_service, user_dep
from services.auth_service import AuthService
from services.user_service import UserService
from config import config_setting
# from services.user_service_impl import UserService
from services.load_service import LoadService
# from api.v1.dependencies import get_user_service, get_load_service

router = APIRouter(prefix="/avatar", tags=["Avatar"])


@router.post(
    "/upload-avatar", 
    status_code=status.HTTP_200_OK,
    summary="Upload user avatar to S3",
    responses={
        401: {"description": "Unauthorized"},
        400: {"description": "No file provided"},
        500: {"description": "Failed to upload avatar"},
    },
)
async def upload_avatar(
    avatar: UploadFile = File(...),
    current_user=Depends(get_current_user),
    user_service: UserService = Depends(user_dep),
    load_service: LoadService = Depends(get_load_service),
) -> dict:
    user_id = current_user.get("id") if isinstance(current_user, dict) else getattr(current_user, "id", None)
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid user data")

    # 1. Завантажуємо на S3
    avatar_url = await load_service.upload_image_to_s3(avatar)

    # 2. Оновлюємо користувача
    await user_service.update_user_avatar(user_id, avatar_url)

    return {"avatar_url": avatar_url}
