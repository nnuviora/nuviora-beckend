from typing import Annotated

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException

from services.auth_service import AuthService
from repositories.user_repo import UserRepository, TokenRepository
from core.security import JWTAuth
from utils.cache_manager import RedisManager
from utils.template_render import get_template

# from utils.email_manager import AwsSender
from utils.email_manager import MetaUaSender

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def auth_dep() -> AuthService:
    return AuthService(
        user_repo=UserRepository,
        refresh_repo=TokenRepository,
        cache_manager=RedisManager,
        email_manager=MetaUaSender,
        security_layer=JWTAuth,
        error_handler=HTTPException,
        template_handler=get_template,
    )


# email_manager=AwsSender,


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], service=Depends(auth_dep)
):
    payload = await service.security_layer.decode_token(token=token)
    if not payload:
        raise Exception("Invalid Token")

    user_id = payload.get("id")

    user = await service.user_repo.get(id=user_id)
    if user is None or user is False:
        raise Exception("User not found")
    return user
