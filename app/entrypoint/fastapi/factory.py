from typing import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.application import application_startup, application_shutdown
from app.entrypoint.fastapi.exceptions import setup_exceptions_handler
from app.entrypoint.fastapi.routers import routers
from app.config.config import config


def create_app() -> FastAPI:

    async def app_startup(application: FastAPI) -> None:
        print("App starting up.")
        await application_startup()

    async def app_shutdown(application: FastAPI) -> None:
        print("App shutting down.")
        await application_shutdown()

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncGenerator:
        await app_startup(application)
        yield
        await app_shutdown(application)

    app: FastAPI = FastAPI(
        title=config.app.title,
        description=config.app.description,
        version=config.app.version,
        lifespan=lifespan,
    )

    for router in routers:
        app.include_router(router)

    setup_exceptions_handler(app)

    return app
