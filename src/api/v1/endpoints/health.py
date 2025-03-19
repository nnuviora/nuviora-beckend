from typing import Annotated

from fastapi.routing import APIRouter
from fastapi import status, Depends


router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", status_code=status.HTTP_200_OK)
async def health() -> str:
    return "OK"