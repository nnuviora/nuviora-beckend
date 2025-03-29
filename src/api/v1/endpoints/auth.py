from typing import Annotated
import uuid

import httpx

from fastapi.routing import APIRouter
from fastapi import status, Depends, Request, Response, HTTPException

from schemas.auth_schema import (
    LoginSchema,
    TokenSchema,
    RegisterSchema,
    ChechEmailSchema,
    ChangePassword
)
from services.auth_service import AuthService
from api.v1.dependencies import auth_dep

from config import config_setting


router = APIRouter(prefix="/auth", tags=["Auth"])

auth_depends = Annotated[AuthService, Depends(auth_dep)]


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    responses={
        405: {"description": "Metod Not Allow"},
        409: {"description": "Email is already taken"},
        400: {"description": "Password Doesn`t Match"},
        500: {"description": "Internal Server Error"},
        504: {"description": "External Service Is Not Responding"},
    },
)
async def register(
    service: auth_depends, data: RegisterSchema
) -> dict:
    data = data.model_dump()
    data["auth_type"] = "local"
    service_action = await service.create_handler(data=data)
    return service_action


@router.get(
    "/verify_email/{token}",
    status_code=status.HTTP_200_OK,
    responses={
        400: {"description": "Email verification token has expired"},
        405: {"description": "Metod Not Allow"},
        500: {"description": "Internal Server Error"},
    },
)
async def verify_email(
    service: auth_depends, token: str, request: Request ,response: Response
) -> TokenSchema:
    data = {
        "user_agent": request.headers.get("User-Agent"),
        "token": token
    }
    service_action = await service.email_verify_handler(data=data)
    response.set_cookie(
        key="refresh_token",
        value=service_action["refresh_token"],
        httponly=True,
        secure=False,
        samesite="strict",
    )
    return {"access_token": service_action["access_token"]}


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "Invalid username or password"},
        405: {"description": "Metod Not Allow"},
        500: {"description": "Internal Server error"},
    },
)
async def login(
    service: auth_depends, data: LoginSchema, request: Request, response: Response
) -> TokenSchema:
    data = data.model_dump()
    data["user_agent"] = request.headers.get("User-Agent")
    service_action = await service.login_handler(data=data)
    response.set_cookie(
        key="refresh_token",
        value=service_action.get("refresh_token"),
        httponly=True,
        secure=False,
        samesite="strict",
    )
    return service_action


@router.get(
    "/resend_email/{user_id}",
    status_code=status.HTTP_200_OK,
    responses={
        400: {"description": "Email verification token has expired"},
        405: {"description": "Metod Not Allow"},
        429: {"description": "Too Many Request"},
        500: {"description": "Internal Server Error"},
        504: {"description": "External Service Is Not Responding"},
    },
)
async def resend_email(user_id: uuid.UUID, service: auth_depends):
    service_action = await service.resend_email(user_id=user_id)
    return service_action


@router.get(
    "/google_auth",
    status_code=status.HTTP_200_OK,
    responses={
        405: {"description": "Metod Not Allow"},
        500: {"description": "Internal Server Error"},
        },
)
async def google_auth():
    params = {
        "client_id": config_setting.GOOGLE_CLIENT_ID,
        "redirect_uri": config_setting.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }
    query_params = "&".join(f"{k}={v}" for k, v in params.items())
    return {"url": f"{config_setting.GOOGLE_AUTH_URL}?{query_params}"}


@router.get(
    "/google/callback",
    status_code=status.HTTP_200_OK,
    responses={
        405: {"description": "Metod Not Allow"},
        500: {"description": "Internal Server Error"},
        },
)
async def auth_callback(
    request: Request, response: Response, service: auth_depends
) -> TokenSchema:
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Doesn`t code auth")

    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            config_setting.GOOGLE_TOKEN_URL,
            data={
                "code": code,
                "client_id": config_setting.GOOGLE_CLIENT_ID,
                "client_secret": config_setting.GOOGLE_CLIENT_SECRET,
                "redirect_uri": config_setting.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
        token_data = token_response.json()
        access_token = token_data["access_token"]

        userinfo_response = await client.get(
            config_setting.GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        data = userinfo_response.json()
        data["auth_type"] = "google"
        data["user_agent"] = request.headers.get("User-Agent")
        service_action = await service.create_handler(data=data)

        response.set_cookie(
            key="refresh_token",
            value=service_action.get("refresh_token"),
            httponly=True,
            secure=False,
            samesite="strict",
        )
    return service_action


@router.post(
    "/refresh_access",
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "Unauthorized"}, 
        404: {"description": "User Not Found"},
        405: {"description": "Metod Not Allow"},
        500: {"description": "Internal Server Error"},
        },
)
async def refresh_access(
    sevice: auth_depends, request: Request, response: Response
) -> TokenSchema:
    data = {
        "refresh_token": request.cookies.get("refresh_token"),
        "user_agent": request.headers.get("User-Agent")
    }
    service_action = await sevice.recreate_access_handler(data=data)
    response.set_cookie(
        key="refresh_token",
        value=service_action.get("refresh_token"),
        httponly=True,
        secure=False,
        samesite="strict",
    )
    return service_action


@router.post(
    "/forgot_password",
    status_code=status.HTTP_200_OK,
    responses={
        404: {"description": "User Not Found"},
        405: {"description": "Metod Not Allow"},
        500: {"description": "Internal Server Error"},
        },
)
async def forgot_password(data: ChechEmailSchema, service: auth_depends) -> dict:
    data = data.model_dump()
    service_action = await service.forgot_password_handler(data=data)
    return service_action


@router.get(
        "/forgot_password/{token}",
        status_code=status.HTTP_200_OK,
        responses={
            200: {"description": "User Verify Successfilly"},
            405: {"description": "Metod Not Allow"},
            500: {"description": "Internal Server Error"},
        }
    )
async def check_user_verify(token: str, service: auth_depends) -> dict:
    service_action = await service.user_verify_handler(token=token)
    return service_action


@router.post(
        "/forgot_password/change",
        status_code=status.HTTP_200_OK,
        responses={
            400: {"description": "Time expired"},
            401: {"description": "Password Doesn`t Match"},
            405: {"description": "Metod Not Allow"},
            500: {"description": "Internal Servet Error"}
        }
)
async def change_password(data: ChangePassword, request: Request, response: Response, service: auth_depends) -> TokenSchema:
    data = data.model_dump()
    data["user_agent"] = request.headers.get("User-Agent")
    service_action = await service.change_password_handler(data=data)
    response.set_cookie(
        key="refresh_token",
        value=service_action.get("refresh_token"),
        httponly=True,
        secure=False,
        samesite="strict",
    )
    return service_action


@router.get(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        405: {"description": "Metod Not Allow"},
        500: {"description": "Internal server error"},
        },
)
async def logout(request: Request, service: auth_depends):
    refresh_token = request.cookies.get("refresh_token")
    service_action = await service.logout_handler(refresh_token=refresh_token)
    return service_action


@router.delete("/delete/{email}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_email_test(email: str, service: auth_depends):
    service_action = await service.delete_test(email=email)
    return service_action
