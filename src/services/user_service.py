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
                raise self.error_handler(status_code = 404, detail="User not found")
            return user_info_dict
        except self.error_handler as e:
            raise e
        except Exception as e:
            raise Exception(f"User not found {self.get_one_user}: {e}")
