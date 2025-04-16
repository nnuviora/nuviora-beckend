import uuid
from typing import Protocol
from utils.repository import AbstractRepository


class UserService(Protocol):
    def __init__(self, user_repo, error_handler) -> None:
        self.user_repo: AbstractRepository = user_repo()
        self.error_handler = error_handler


    async def get_one_user(self, uuid: str) -> dict:
        try:
            user_info_dict = await self.user_repo.get(id=uuid)
            print(user_info_dict)
            if not user_info_dict:
                raise self.error_handler(status_code=404, detail="User not found")
            return user_info_dict
        except self.error_handler as e:
            raise e
        except Exception as e:
            raise Exception(f"User not found {self.get_one_user}: {e}")
        

    async def delete_one_user (self, uuid: str):
        try:
            #geting the user
            user_to_delete = await self.user_repo.get(id = uuid)
            print (f"User_to delete {user_to_delete}")

            #check if the user exists
            if not user_to_delete:
                raise self.error_handler(status_code=404, detail="User does not exist")
            
            #delete user
            await self.user_repo.delete(id = uuid)
            return {"message": "The user was deleted seccesfully"}
        
        except self.error_handler as e:
            raise e
        except Exception as e:
            raise Exception (f"User to delete not found {self.delete_one_user}: {e}")
        
    
    async def update_user(self, user_id: uuid, update_data: dict):
        try:
            user = await self.user_repo.get(id=user_id)
            if not user:
                raise self.error_handler(status_code=404, detail="User for update not found")

            updated_user = await self.user_repo.update(id=user_id, update_fields=update_data)
            return updated_user
        except self.error_handler as e:
            raise e
        except Exception as e:
            raise Exception(f"User update failed: {e}")

