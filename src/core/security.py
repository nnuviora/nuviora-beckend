from datetime import timedelta, datetime, timezone

from passlib.context import CryptContext
import jwt


class SecurityBase:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)
    
    async def verify_password(self, password: str, hash_password: str) -> bool:
        return self.pwd_context.verify(password, hash_password)
    

class JWTAuth(SecurityBase):
    SECRET_KEY = None
    ALGORITHM = None

    def __init__(self):
        pass

    async def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> dict:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    async def create_refresh_token(self) -> dict:
        pass