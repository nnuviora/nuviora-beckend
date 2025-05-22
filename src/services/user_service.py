import uuid
from typing import Protocol
from utils.repository import AbstractRepository
from repositories.user_repo import TokenRepository
from schemas.user_schema import UserUpdateAvatar
from core.security import SecurityBase

class UserService(Protocol):
    def __init__(self, 
                 user_repo, 
                 error_handler, 
                 token_repo,
                 security_layer
        ) -> None:
        self.user_repo: AbstractRepository = user_repo
        self.error_handler = error_handler
        self.token_repo: TokenRepository = token_repo
        self.security_layer: SecurityBase = security_layer


    async def get_one_user(self, user_id: str) -> dict:
        try:
            user_info_dict = await self.user_repo.get(id=user_id)
            print(user_info_dict)
            if not user_info_dict:
                raise self.error_handler(status_code=404, detail="User not found")
            return user_info_dict
        except self.error_handler as e:
            raise e
        except Exception as e:
            raise Exception(f"The user cannot be found")
        

    async def delete_one_user(self, uuid):
        try:
            # geting the user
            user_to_delete = await self.user_repo.get(id=uuid)

            # check if the user exists
            if not user_to_delete:
                raise self.error_handler(status_code=404, detail="User does not exist")

            # deleting user tokens
            await self.token_repo.delete(user_id=uuid)

            # delete user
            await self.user_repo.delete(id=uuid)
            return {"message": "The user was deleted seccesfully"}

        except self.error_handler as e:
            raise e
        except Exception as e:
            raise Exception(f"User to delete not found")
        

    async def update_user(self, user_id: uuid.UUID, update_data: dict):

        try:
            user = await self.user_repo.get(id=user_id)
            if not user:
                raise self.error_handler(
                    status_code=404, detail="User for update not found"
                )

            updated_user = await self.user_repo.update(id=user_id, data=update_data)
            return updated_user

        except self.error_handler as e:
            raise e
        except Exception as e:
            raise Exception(f"User update has failed")
        

    async def update_user_avatar(self, user_id: uuid.UUID, avatar_url: str):
        try:
            user = await self.user_repo.get(id=user_id)
            if not user:
                raise self.error_handler(status_code=404, detail="User for update not found")

            updated_user_avatar = await self.user_repo.update(id=user_id, data={"avatar": avatar_url})
            if not updated_user_avatar:
                raise self.error_handler(status_code=500, detail="Failed to update user avatar")

            return updated_user_avatar

        except Exception as e:
            raise self.error_handler(status_code=500, detail=f"User avatar update failed: {str(e)}")
        

    async def change_user_password (self, 
                                    user_id: uuid.UUID, 
                                    new_password: dict):
        try:
             
            user = await self.user_repo.get(id=user_id)
            if not user:
                raise self.error_handler(status_code=404, detail="User for update not found")
            
            plain_password = new_password.get("new_password") 
            hashed_password = await self.security_layer.hash_password(plain_password)

            user_with_new_pass = await self.user_repo.update(
                id=user_id, 
                data={"hash_password": hashed_password}
            )
            return user_with_new_pass
        


        except self.error_handler as e:
            raise e
        except Exception as e:
            raise Exception(f"The user is not found")
