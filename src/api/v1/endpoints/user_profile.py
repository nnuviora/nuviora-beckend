from typing import Annotated
from fastapi.routing import APIRouter
from fastapi import status, Depends, Request, Response, HTTPException
from repositories.user_repo import UserRepository
from services.user_service import UserService
from schemas.user_schema import UserBaseSchema
from api.v1.dependencies import get_current_user, user_dep


router = APIRouter(prefix="/user", tags=["User Profile"])

one_user_dependencies = Annotated[UserService, Depends(user_dep)]


@router.get("/{uuid}", status_code=status.HTTP_200_OK)
async def get_one_user(
    uuid: str, user_service: one_user_dependencies
) -> UserBaseSchema:
    try:
        user_data = await user_service.get_one_user(uuid)
        return user_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
