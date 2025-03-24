import uuid
from typing import Annotated

from fastapi.routing import APIRouter
from fastapi import status, Depends, Request, Response

from schemas.auth_schema import LoginSchema, TokenSchema, RegisterSchema
from services.auth_service import AuthService
from api.v1.dependencies import auth_dep


router = APIRouter(prefix="/auth", tags=["Auth"])

auth_depends = Annotated[AuthService, Depends(auth_dep)]


@router.post("/register", status_code=status.HTTP_200_OK)
async def register(
    request: Request, service: auth_depends, data: RegisterSchema
) -> dict:
    print(request.headers)
    data = data.model_dump(exclude=["id"])
    data["user_agent"] = request.headers["User-Agent"]
    data["auth_type"] = "username"
    service_action = await service.create_handler(data=data)
    return service_action


@router.get("/verify_email/{token}", status_code=status.HTTP_200_OK)
async def verify_email(
    service: auth_depends, token: str, response: Response
) -> TokenSchema:
    service_action = await service.verify_handler(token=token)
    response.set_cookie(
        key="refresh_token",
        value=service_action["refresh_token"],
        httponly=True,
        secure=True,
        samesite="strict",
    )
    return {"access_token": service_action["access_token"]}


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    service: auth_depends, data: LoginSchema, request: Request, response: Response
) -> TokenSchema:
    data = data.model_dump()
    data["user_agent"] = request.headers["User-Agent"]
    service_action = await service.login_handler(data=data)
    response.set_cookie(
        key="refresh_token",
        value=service_action["refresh_token"],
        httponly=True,
        secure=True,
        samesite="strict",
    )
    return service_action


@router.post("/refresh_access", status_code=status.HTTP_200_OK)
async def refresh_access(sevice: auth_depends, request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    service_action = await sevice.recreate_access_handler(refresh_token=refresh_token)
    response.set_cookie(
        key="refresh_token",
        value=service_action["refresh_token"],
        httponly=True,
        secure=True,
        samesite="strict",
    )
    return {"access_token": service_action["access_token"]}


@router.get("/logout", status_code=status.HTTP_200_OK)
async def logout(service: auth_depends):
    pass
