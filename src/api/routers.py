from .v1.endpoints.health import router as health_router
from .v1.endpoints.auth import router as auth_router

routers = [health_router, auth_router]
