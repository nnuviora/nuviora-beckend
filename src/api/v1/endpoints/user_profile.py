from typing import Annotated
from fastapi.routing import APIRouter
from fastapi import status, Depends, Request, Response, HTTPException
from repositories.user_repo import UserRepository
from services.user_service import UserService
from schemas.user_schema import UserBaseSchema, UserUpdateSchema, UserChangePasswrdSchema
from api.v1.dependencies import get_current_user, user_dep, get_load_service
from fastapi import UploadFile, File
from services.load_service import LoadService




router = APIRouter(prefix="/profile", tags=["User Profile"])


user_service_dep = Annotated[UserService, Depends(user_dep)]
user_base_schema_dep = Annotated[UserBaseSchema, Depends(get_current_user)]


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "Неправильний або відсутній токен"},
        500: {"description": "Упс! Щось пішло не так, спробуйте пізніше"},
    },
)
async def profile(user: user_base_schema_dep) -> UserBaseSchema:
    return user


@router.delete(
    "/delete_user",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"description": "Неправильний або відсутній токен"},
        403: {"description": "у вас немає прав щоб видалити користувача"},
        404: {"description": "Такого користувача не існує"},
        500: {"description": "Упс! Щось пішло не так, спробуйте пізніше"},
    },
)
async def delete_user(
    current_user: user_base_schema_dep, 
    user_service: user_service_dep
):

    user_id = current_user.get("id")
    await user_service.delete_one_user(uuid=user_id)
    return {"message": f"Користувач {current_user.get('id')} успішно видалений"}


@router.put(
    "/update_user_info",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Інформація оновлена успішно"},
        400: {"description": "Неправильний запит"},
        401: {"description": "Немає прав доступу"},
        403: {"description": "Заборонено"},
        404: {"description": "Такого користувача не існує"},
        409: {"description": "Конфлікт з існуючими даними"},
        422: {"description": "Помилка валідації"},
    },
)
async def update_user_info(
    dep: user_base_schema_dep,
    new_data: UserUpdateSchema,
    user_service: user_service_dep,
):
    new_data = new_data.model_dump(
        exclude_none=True
    )
    updated_user = await user_service.update_user(
        user_id=dep["id"], update_data=new_data
    )
    return updated_user


@router.put(
    "/change_password", status_code=status.HTTP_200_OK,
        responses={
        200: {"description": "Пароль оновлено успішно"},
        400: {"description": "Неправильний запит"},
        401: {"description": "Немає прав доступу"},
        403: {"description": "Заборонено"},
        404: {"description": "Такого користувача не існує"},
        409: {"description": "Конфлікт з існуючими даними"},
        422: {"description": "Помилка валідації, паролі не співпадють?"},
    },
)
async def update_user_password(
    current_user: user_base_schema_dep,
    user_service: user_service_dep,
    new_password: UserChangePasswrdSchema
):
    """
    Update the password for the current authenticated user.

    Args:
        current_user (user_base_schema_dep): The currently authenticated user, provided via dependency injection.
        user_service (user_service_dep): Service layer for user operations.
        new_password (UserChangePasswrdSchema): Schema containing the current and new password.

    Raises:
        HTTPException: If the current password is incorrect (403 Forbidden).

    Returns:
        dict: A success message indicating the password was updated.
    """
    
    is_valid = await user_service.security_layer.verify_password(
        password=new_password.current_password,
        hash_password=current_user["hash_password"]
    )
    if not is_valid:
        raise HTTPException(status_code=403, detail="Неправильний поточний пароль")
    


    
    user_with_new_pass = await user_service.change_user_password(
        user_id=current_user["id"],
        new_password={"new_password": new_password.new_password}
    )
    #DELETE print statement IN PRODUCTION
    print (f"Passwoprd for user {user_with_new_pass.get('email')} was updated succesfully")
    return {"message": f"Пароль для користувача: {current_user.get('id')} успішно оновлений"}

###########################################################################################
#AVATAR UPLOAD AND GET
###########################################################################################


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

###########################################################################################


@router.get(
    "/get-avatar", 
    status_code=status.HTTP_200_OK,
    summary="Get user avatar from S3",
    responses={
        401: {"description": "Unauthorized"},
        400: {"description": "No file found"},
        500: {"description": "Failed to read avatar"},
    },
)
async def get_avatar(
    current_user: user_base_schema_dep,
    user_service: user_service_dep,
    ):
    user_id = current_user.get("id")
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid user data")
    
    
    all_info_about_curr_user = await user_service.get_one_user(user_id=user_id)
    avatar_url_for_curr_user = all_info_about_curr_user.get("avatar")
    if not avatar_url_for_curr_user:
        raise HTTPException(status_code=400, detail="Avatar not found")
    
    return {"avatar_url": avatar_url_for_curr_user}