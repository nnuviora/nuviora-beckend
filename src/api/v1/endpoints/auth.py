import uuid
from typing import Annotated

from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi import status, Depends

from schemas.user_schema import UserInDb
from services.auth_service import AuthService
from api.v1.dependencies import auth_dep


router = APIRouter(prefix="/auth", tags=["Auth"])

auth_depends = Annotated[AuthService, Depends(auth_dep)]


@router.post("/register", status_code=status.HTTP_200_OK)
async def register(request: Request, service: auth_depends, data: UserInDb) -> dict:
    data = data.model_dump(exclude=["id"])
    data["user_agent"] = request.headers["User-Agent"]
    service_action = await service.create_handler(data=data)
    return service_action


@router.get("/verify_email/{token}", status_code=status.HTTP_200_OK)
async def verify_email(service: auth_depends, token: uuid.UUID) -> None:
    service_action = await service.verify_handler(token=token)
    return service_action


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(service: auth_depends, data: None) -> None:
    service_action = await service.login_handler(data=data)
    return service_action


@router.post("/refresh_access", status_code=status.HTTP_200_OK)
async def refresh_access(sevice: auth_depends, data: None):
    pass


@router.get("/logout", status_code=status.HTTP_200_OK)
async def logout(service: auth_depends):
    pass
