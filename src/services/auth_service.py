from typing import Protocol

from utils.repository import AbstractRepository
from utils.cache_manager import AbstractCache
from utils.email_manager import AbstractEmail


class AuthService(Protocol):
    def __init__(
        self, user_repo, refresh_repo, cache_manager, email_manager, security_layer
    ) -> None:
        self.user_repo: AbstractRepository = user_repo()
        self.refesh_repo: AbstractRepository = refresh_repo()
        self.cache_manager: AbstractCache = cache_manager()
        self.email_manager: AbstractEmail = email_manager()
        self.security_layer = security_layer()

    async def create_handler(self, data: dict) -> dict:
        try:
            if data["auth_type"] == "username":
                data["hash_password"] = await self.security_layer.hash_password(
                    password=data["hash_password"]
                )
                cache_data = await self.cache_manager.set(data=data)
                print(cache_data)
                email = await self.email_manager.send_email(
                    recipient=data["email"],
                    subject="Email Verification",
                    body_text=f"http://localhost/auth/verify_email/{str(cache_data)}",
                )
                return {"message": "Message sended"}

            obj = await self.user_repo.insert(data=data)
            return obj
        except Exception as e:
            raise Exception(f"Create Error in {self.create_handler.__name__}: {e}")

    async def verify_handler(self, token: str) -> dict:
        try:
            data = await self.cache_manager.get(token=token)
            user_agent = data.pop("user_agent")
            user_obj = await self.user_repo.insert(data=data)

            if not data:
                raise Exception("Error Time")

            access_token = await self.security_layer.create_access_token(
                data={"id": str(user_obj["id"])}
            )
            refresh_token, expire = await self.security_layer.create_refresh_token(
                data={"id": str(user_obj["id"])}
            )
            token = await self.refesh_repo.insert(
                data={
                    "user_id": user_obj["id"],
                    "refresh_token": refresh_token,
                    "user_agent": user_agent,
                    "expires_at": expire,
                }
            )
            return {
                "access_token": access_token,
                "refresh_token": token["refresh_token"],
            }
        except Exception as e:
            raise Exception(f"Error in {self.verify_handler.__name__}: {e}")

    async def login_handler(self, data: dict) -> dict:
        try:
            user_obj = await self.user_repo.get(email=data["login"])
            if not user_obj:
                raise Exception("Wrong login or password")  #
            if not (
                await self.security_layer.verify_password(
                    password=data["password"], hash_password=user_obj["hash_password"]
                )
            ):
                raise Exception("Wrong login or password")  #
            access_token = await self.security_layer.create_access_token(
                data={"id": str(user_obj["id"])}
            )
            refresh_token, expire = await self.security_layer.create_refresh_token(
                data={"id": str(user_obj["id"])}
            )
            token = await self.refesh_repo.insert(
                data={
                    "user_id": user_obj["id"],
                    "refresh_token": refresh_token,
                    "user_agent": data["user_agent"],
                    "expires_at": expire,
                }
            )
            return {
                "access_token": access_token,
                "refresh_token": token["refresh_token"],
            }
        except Exception as e:
            raise Exception(f"Login Error in {self.login_handler.__name__}: {e}")

    async def recreate_access_handler(self, refresh_token: str) -> dict:
        try:
            payload = await self.security_layer.decode_token(token=refresh_token)
            if payload:
                user_obj = await self.user_repo.get(id=payload["id"])
                if user_obj:
                    access_token = await self.security_layer.create_access_token(
                        data={"id": str(user_obj["id"])}
                    )
                    return {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    }
                else:
                    raise Exception("")  #
            else:
                raise Exception("")  #
        except Exception as e:
            raise Exception(
                f"Refresh Error in {self.recreate_access_handler.__name__}: {e}"
            )

    async def logout_handler(self):
        pass
