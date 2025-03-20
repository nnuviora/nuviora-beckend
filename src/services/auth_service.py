import asyncio
from typing import Protocol

from utils.repository import AbstractRepository
from utils.cache_manager import AbstractCache
from utils.email_manager import AbstractEmail


class AuthService(Protocol):
    def __init__(
            self, 
            user_repo, 
            cache_manager, 
            email_manager,
            security_layer
            ) -> None:
        self.user_repo: AbstractRepository = user_repo()
        self.cache_manager: AbstractCache = cache_manager()
        self.email_manager: AbstractEmail = email_manager()
        self.security_layer = security_layer()

    async def create_handler(self, data: dict) -> dict:
        try:
            if data["auth_type"] == "login":
                data["hash_password"] = await self.security_layer.hash_password(
                    password=data["hash_password"]
                    )
                cache_data = await self.cache_manager.set(data=data)
                email = await self.email_manager.send_email(
                    recipient=data["email"],
                    subject=None
                )
                return {"message": None}

            obj = await self.user_repo.insert(data=data)
            return obj 
        except Exception as e:
            raise Exception(f"Create Error in {self.create_handler.__name__}: {e}")

    async def verify_handler(self, token: str) -> dict:
        try:
            data = await self.cache_manager.get(token=token)
            obj = await self.user_repo.insert(data=data)
            
            if not obj:
                raise Exception("Error Time")

            access_token, refresh_token = asyncio.gather(
                self.create_access_token(),
                self.create_refresh_token()
            )
            return {"access_token": access_token, "refresh_token": refresh_token} 
        except Exception as e:
            raise Exception(f"Error in {self.email_confirmed.__name__}: {e}")

    async def login_handler(self, data: dict) -> dict:
        try:
            obj = await self.user_repo.get(email=data["email"])
            if not obj:
                return None #Warning
            if not (await self.security_layer.verify_password(
                password=data["password"],
                hash_password=obj["hash_password"] 
                )):
                return None #Warning
            access_token, refresh_token = asyncio.gather(
                self.create_access_token(),
                self.create_refresh_token()
            )
            return {"access_token": access_token, "refresh_token": refresh_token}
        except Exception as e:
            raise Exception(f"Login Error in {self.login_handler.__name__}: {e}")
        
    async def recreate_access_handler(self, refresh_token: str) -> dict:
        pass

    async def logout_handler(self):
        pass