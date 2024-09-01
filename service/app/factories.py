from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from service.app import deployment_time
from service.app.routers.health import health_router
from service.app.routers.requests import request_router
from service.utils.logs import initialize_logging


def create_api() -> FastAPI:

    initialize_logging("config/logging.yaml")

    api = FastAPI()
    api.include_router(health_router)
    api.include_router(request_router)

    deployment_time.set(datetime.now(tz=timezone.utc).isoformat())

    add_pagination(api)

    return api
