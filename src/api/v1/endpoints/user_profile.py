from typing import Annotated
from fastapi.routing import APIRouter
from fastapi import status, Depends, Request, Response, HTTPException
from repositories.user_repo import UserRepository
from services.user_service import UserService
from schemas.user_schema import UserBaseSchema, UserUpdateSchema
from api.v1.dependencies import get_current_user, user_dep


router = APIRouter(prefix="/user", tags=["User Profile"])

one_user_dependencies = Annotated[UserService, Depends(user_dep)]
current_user_dep = Annotated[UserBaseSchema, Depends(get_current_user)]




@router.get("/{uuid}", status_code=status.HTTP_200_OK)
async def get_one_user(
    uuid: str, user_service: one_user_dependencies
) -> UserBaseSchema:
    try:
        user_data = await user_service.get_one_user(uuid)
        return user_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@router.delete ("/delete_user", status_code=status.HTTP_200_OK)
async def delete_user (dep:current_user_dep ):
    return {"message": f"User {dep.id} deleted"}


@router.put ("/update_user_info", status_code=status.HTTP_200_OK)
async def update_user_info (
    dep:current_user_dep,
    new_data: UserUpdateSchema,
    user_service: one_user_dependencies
    ):
    try:
        updated_user = await user_service.update_user(dep.id, update_data=new_data)
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    


