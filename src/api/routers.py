from .v1.endpoints.health import router as health_router
from .v1.endpoints.auth import router as auth_router
from .v1.endpoints.user_profile import router as one_user_router


routers = [
    health_router,
    auth_router,
    one_user_router,
]
