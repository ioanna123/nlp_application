from typing_extensions import TypedDict

from fastapi import APIRouter

from service import __version__
from service.app import deployment_time

health_router = APIRouter(prefix="/health", tags=['health'])


class HealthInfo(TypedDict):
    status: str
    version: str
    deployed: str


@health_router.get(path="/", response_model=HealthInfo, status_code=200)
def health():
    return {
        "status": "OK",
        "version": __version__,
        "deployed": deployment_time.get()
    }
