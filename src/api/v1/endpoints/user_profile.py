from typing import Annotated
from fastapi.routing import APIRouter
from fastapi import status, Depends, Request, Response, HTTPException
from repositories.user_repo import UserRepository
from services.user_service import UserService
from schemas.user_schema import UserBaseSchema, UserUpdateSchema
from api.v1.dependencies import get_current_user, user_dep


router = APIRouter(prefix="/profile", tags=["User Profile"])


user_service_dep = Annotated[UserService, Depends(user_dep)]
user_base_schema_dep = Annotated[UserBaseSchema, Depends(get_current_user)]



@router.get("/me", status_code=status.HTTP_200_OK,
            responses={
            401: {"description": "Unauthorized: Invalid or missing token"},
            500: {"description": "Internal Server Error"},
            },
            )
async def profile(user: user_base_schema_dep) -> UserBaseSchema:
    return user


@router.delete(
    "/delete_user",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"description": "Unauthorized: Invalid or missing token"},
        403: {"description": "Forbidden: No permission to delete user"},
        404: {"description": "User not found"},
        500: {"description": "Internal Server Error"},
    },
)
async def delete_user(
    current_user: user_base_schema_dep, user_service: user_service_dep
):

    user_id = current_user.get("id")
    await user_service.delete_one_user(uuid=user_id)
    return {"message": f"User {current_user.get('id')} succesfully deleted"}


@router.put(
    "/update_user_info",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "User info updated successfully"},
        400: {"description": "Invalid request"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "User not found"},
        409: {"description": "Conflict with existing data"},
        422: {"description": "Validation error"},
    },
)
async def update_user_info(
    dep: user_base_schema_dep,
    new_data: UserUpdateSchema,
    user_service: user_service_dep,
):
    new_data = new_data.model_dump(
        exclude_none=True
    )  # converting to dict # 2) excluding NULL values passed ftom the user
    updated_user = await user_service.update_user(
        user_id=dep["id"], update_data=new_data
    )
    return updated_user
