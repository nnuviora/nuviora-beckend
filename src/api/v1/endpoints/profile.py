from typing import Annotated

from fastapi.routing import APIRouter
from fastapi import Depends, status

from schemas.user_schema import UserBaseSchema
from api.v1.dependencies import get_current_user


router = APIRouter(prefix="/profile", tags=["Profile"])


auth_depend = Annotated[UserBaseSchema, Depends(get_current_user)]


@router.get("/me", status_code=status.HTTP_200_OK)
async def profile(user: auth_depend) -> UserBaseSchema:
    return user
