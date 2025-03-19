from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

from database import engine, Base
from api.routers import routers
from admin.routes import routes


def get_application() -> FastAPI:

    async def startup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    application = FastAPI()
    # admin = Admin(app=application, engine=engine)

    application.add_event_handler("startup", startup)

    origins = []

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # for view in routes:
    #     admin.add_view(view)

    for router in routers:
        application.include_router(router=router)

    return application


app = get_application()