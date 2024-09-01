import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from fastapi_pagination import Page
from pydantic import ValidationError

from service.app.auth import create_jwt_bearer
from service.controller.controller import BaseController
from service.controller.errors import RequestDoesNotExist
from service.controller.factory import create_base_controller
from service.data_model.request import NLPModel, search_params_to_data_model, NLPRequest
from service.data_model.status import Status

logger = logging.getLogger(__name__)
request_router = APIRouter(prefix="/request", dependencies=[Depends(create_jwt_bearer())],
                           tags=['request'])

controller: BaseController = create_base_controller()


@request_router.get(path="/{request_id}/", response_model=NLPModel, status_code=200)
def retrieve_job(request_id: str):
    try:
        logger.info(f"Get request for job: {request_id}")
        return controller.retrieve(request_id)
    except RequestDoesNotExist:
        raise HTTPException(404, f"NLP request {request_id} not found")
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, "Unexpected error")


@request_router.get(path="/", response_model=Page[NLPModel], status_code=200)
def search_jobs(
        status: Optional[Status] = None,
        client: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None):
    try:
        search_query = search_params_to_data_model(
            status=status, client=client, date_from=date_from, date_to=date_to
        )
        logger.info(f"Running search for pairwise request with params: {search_query}")
        return controller.search(search=search_query)
    except ValidationError:
        raise HTTPException(422, "Invalid query params")
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, "Unexpected error")


@request_router.post(path="/", response_model=NLPModel, status_code=202)
@request_router.post(path="", response_model=NLPModel, status_code=202, include_in_schema=False)
def create_job(request: NLPRequest):
    try:
        return controller.predict(request)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, "Unexpected error")
