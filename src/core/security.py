from datetime import (
    timedelta,
    datetime,
    timezone,
)

from passlib.context import CryptContext
import jwt

from config import config_setting


class SecurityBase:
    def __init__(self):
        self.pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
        )

    async def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def verify_password(
        self,
        password: str,
        hash_password: str,
    ) -> bool:
        return self.pwd_context.verify(password, hash_password)


class JWTAuth(SecurityBase):
    SECRET_KEY = config_setting.SECRET_KEY
    ALGORITHM = config_setting.ALGORITHM

    def __init__(self):
        super().__init__()

    async def create_access_token(self, data: dict) -> str:
        try:
            to_encode = data.copy()
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=config_setting.ACCESS_TOKEN_EXPIRE_MINUTES
            )
            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(
                to_encode,
                self.SECRET_KEY,
                algorithm=self.ALGORITHM,
            )
            return encoded_jwt
        except Exception as e:
            raise Exception(
                f"Create Access Token Error in {self.create_access_token.__name__}: {e}"
            )

    async def create_refresh_token(self, data: dict) -> str:
        try:
            to_encode = data.copy()
            expire = datetime.now(timezone.utc) + timedelta(
                days=config_setting.REFRESH_TOKEN_EXPIRE_DAYS
            )
            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(
                to_encode,
                self.SECRET_KEY,
                algorithm=self.ALGORITHM,
            )
            return (
                encoded_jwt,
                expire.replace(tzinfo=None),
            )
        except Exception as e:
            raise Exception(
                f"Create Refresh Token Error in {self.create_refresh_token.__name__}: {e}"
            )

    async def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                self.SECRET_KEY,
                algorithms=self.ALGORITHM,
            )
            return payload
        except Exception as e:
            raise Exception(f"Decode Token Error in {self.decode_token.__name__}: {e}")
