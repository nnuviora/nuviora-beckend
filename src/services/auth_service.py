from datetime import timedelta
from typing import Protocol

from utils.repository import AbstractRepository

class AuthService(Protocol):
    def __init__(self, user_repo) -> None:
        self.user_repo: AbstractRepository = user_repo()

    async def create_handler(self, data: dict) -> dict:
        return await self.user_repo.insert(data={"username": "Bob"})

    async def email_confirmed(self, token: str) -> dict:
        pass

    async def login_handler(self) -> dict:
        pass
