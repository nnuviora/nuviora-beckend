from services.auth_service import AuthService
from repositories.user_repo import UserRepository
from core.security import JWTAuth
from utils.cache_manager import RedisManager
from utils.email_manager import AwsSender


def auth_dep() -> AuthService:
    return AuthService(
        user_repo=UserRepository,
        cache_manager=RedisManager,
        email_manager=AwsSender,
        security_layer=JWTAuth
    )