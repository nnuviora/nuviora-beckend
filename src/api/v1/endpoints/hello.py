from fastapi.routing import APIRouter
from fastapi import status


router = APIRouter(prefix="/hello")


@router.get("/", status_code=status.HTTP_200_OK)
async def hello() -> str:
    return "Hello, hello?"