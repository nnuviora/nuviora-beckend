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
    ChangePassword,
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
        201: {"description": "Повідомлення надіслано"}, 
        400: {"description": "Паролі не збігаються"},
        405: {"description": "Метод заборонено"},
        409: {"description": "Електронна пошта вже існує"},
        500: {"description": "Упс! Щось пішло не так. Спробуйте пізніше"},
    },
)
async def register(service: auth_depends, data: RegisterSchema) -> dict:
    data = data.model_dump()
    data["auth_type"] = "local"
    service_action = await service.create_handler(data=data)
    return service_action


@router.get(
    "/verify_email/{token}",
    status_code=status.HTTP_200_OK,
    responses={
        400: {"description": "Токен підтвердження електронної пошти протермінований"},
        405: {"description": "Метод заборонено"},
        500: {"description": "Упс! Щось пішло не так. Спробуйте пізніше"},
    },
)
async def verify_email(
    service: auth_depends, token: str, request: Request, response: Response
) -> TokenSchema:
    data = {"user_agent": request.headers.get("User-Agent"), "token": token}
    service_action = await service.email_verify_handler(data=data)
    response.set_cookie(
        key="refresh_token",
        value=service_action.get("refresh_token"),
        path="/",
        httponly=True,
        secure=True,
        samesite="none",
        max_age=7*24*60*60,
        domain="nuviora.click"
    )
    return {
        "access_token": service_action.get("access_token"),
        "user": service_action.get("user"),
    }


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    responses={
        400: {"description": "Недійсне ім'я користувача або пароль"},
        405: {"description": "Метод заборонено"},
        500: {"description": "Упс! Щось пішло не так. Спробуйте пізніше"},
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
        path="/",
        httponly=True,
        secure=True,
        samesite="none",
        max_age=7*24*60*60,
        domain="nuviora.click"
    )
    return {
        "access_token": service_action.get("access_token"),
        "user": service_action.get("user"),
    }


@router.get(
    "/resend_email/{user_id}",
    status_code=status.HTTP_200_OK,
    responses={
        400: {"description": "Токен підтвердження електронної пошти протермінований"},
        405: {"description": "Метод заборонено"},
        429: {"description": "Забагато запитів"},
        500: {"description": "Упс! Щось пішло не так. Спробуйте пізніше"},
    },
)
async def resend_email(user_id: uuid.UUID, service: auth_depends):
    service_action = await service.resend_email(user_id=user_id)
    return service_action


@router.get(
    "/google_auth",
    status_code=status.HTTP_200_OK,
    responses={
        405: {"description": "Метод заборонено"},
        500: {"description": "Упс! Щось пішло не так. Спробуйте пізніше"},
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
        405: {"description": "Метод заборонено"},
        500: {"description": "Упс! Щось пішло не так. Спробуйте пізніше"},
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
            path="/",
            httponly=True,
            secure=True,
            samesite="none",
            max_age=7*24*60*60,
            domain="nuviora.click"
        )
    return service_action


@router.post(
    "/refresh_access",
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "Несанкціонований доступ"},
        404: {"description": "Користувача не знайдено"},
        405: {"description": "Метод заборонено"},
        500: {"description": "Упс! Щось пішло не так. Спробуйте пізніше"},
    },
)
async def refresh_access(
    sevice: auth_depends, request: Request, response: Response
) -> TokenSchema:
    data = {
        "refresh_token": request.cookies.get("refresh_token"),
        "user_agent": request.headers.get("User-Agent"),
    }
    service_action = await sevice.recreate_access_handler(data=data)
    response.set_cookie(
        key="refresh_token",
        value=service_action.get("refresh_token"),
        path="/",
        httponly=True,
        secure=True,
        samesite="none",
        max_age=7*24*60*60,
        domain="nuviora.click"
    )
    return service_action


@router.post(
    "/forgot_password",
    status_code=status.HTTP_200_OK,
    responses={
        404: {"description": "Користувача не знайдено"},
        405: {"description": "Метод заборонено"},
        500: {"description": "Упс! Щось пішло не так. Спробуйте пізніше"},
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
        200: {"description": "Користувача успішно підтверджено"},
        405: {"description": "Метод заборонено"},
        500: {"description": "Упс! Щось пішло не так. Спробуйте пізніше"},
    },
)
async def check_user_verify(token: str, service: auth_depends) -> dict:
    service_action = await service.user_verify_handler(token=token)
    return service_action


@router.post(
    "/forgot_password/change",
    status_code=status.HTTP_200_OK,
    responses={
        400: {"description": "Час вичерпано"},
        401: {"description": "Паролі не збігаються"},
        405: {"description": "Метод заборонено"},
        500: {"description": "Упс! Щось пішло не так. Спробуйте пізніше"},
    },
)
async def change_password(
    data: ChangePassword, request: Request, response: Response, service: auth_depends
) -> dict:
    data = data.model_dump()
    data["user_agent"] = request.headers.get("User-Agent")
    service_action = await service.change_password_handler(data=data)
    response.set_cookie(
        key="refresh_token",
        value=service_action.get("refresh_token"),
        path="/",
        httponly=True,
        secure=True,
        samesite="none",
        max_age=7*24*60*60,
        domain="nuviora.click"
    )
    return service_action


@router.get(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        405: {"description": "Метод заборонено"},
        500: {"description": "Упс! Щось пішло не так. Спробуйте пізніше"},
    },
)
async def logout(request: Request, response: Response, service: auth_depends):
    refresh_token = request.cookies.get("refresh_token")
    service_action = await service.logout_handler(refresh_token=refresh_token)
    response.delete_cookie(
        key="refresh_token",
        path="/",
        domain="nuviora.click",
        samesite="none",
        secure=True
    )
    return service_action


@router.delete("/delete/{email}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_email_test(email: str, service: auth_depends):
    service_action = await service.delete_test(email=email)
    return service_action