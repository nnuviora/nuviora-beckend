from .v1.endpoints.health import router as health_router
from .v1.endpoints.user import router as user_router

routers = [health_router, user_router]
