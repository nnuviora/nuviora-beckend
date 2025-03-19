from passlib.context import CryptContext


class SecurityBase:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def verify_password(self, password: str, hash_password: str) -> bool:
        return self.pwd_context.verify(password, hash_password)


class JWTAuth(SecurityBase):
    def __init__(self):
        pass

    async def create_access_token(self) -> dict:
        pass

    async def create_refresh_token(self) -> dict:
        pass

    async def to_encode(self):
        pass

    async def to_decode(self):
        pass
