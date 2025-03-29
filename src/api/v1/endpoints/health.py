from typing import Annotated

from fastapi.routing import APIRouter
from fastapi import status, Depends

from schemas.user_schema import (
    UserBaseSchema,
)
from api.v1.dependencies import (
    get_current_user,
)


router = APIRouter(prefix="/health", tags=["Health"])


current_user = Annotated[
    UserBaseSchema,
    Depends(get_current_user),
]


@router.get("/", status_code=status.HTTP_200_OK)
async def health(
    user: current_user,
) -> str:
    return "OK"
