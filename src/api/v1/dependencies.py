from services.auth_service import AuthService
from repositories.user_repo import UserRepository


def user_dep() -> AuthService:
    return AuthService(
        user_repo=UserRepository
    )