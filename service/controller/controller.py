import logging
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import List

from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.sql import Select

from service.controller.errors import RequestDoesNotExist, CriticalDBError
from service.data_model.request import SearchQuery, NLPModel, NLPRequest, model_from_orm, model_to_orm
from service.data_model.status import Status
from service.db.errors import UnexpectedDBError
from service.db.schema import NLPModelDBModel
from service.ml.pipelines.pipeline import MLPipeline

logger = logging.getLogger(__name__)


class Controller(ABC):

    def __init__(self, db_engine: Engine):
        self.db_engine = db_engine

    @abstractmethod
    def create(self, request: NLPRequest) -> NLPModel:
        pass

    def retrieve(self, request_id: str) -> NLPModel:
        """
       Retrieves the info given a request id.
       :param request_id: Request id to get.
       :return: The NLPModel
       """
        request = self._get_request_from_db(request_id)
        return model_from_orm(request)

    def search(self, search: SearchQuery) -> NLPModel:
        """
       Fetches a page of results for a given search.
       :param search: The search we want to execute.
       :return: The results of the search query.
       """

        stmt = self._build_query_search(search)

        with self.db_session as session:
            return paginate(session, stmt.order_by(NLPModelDBModel.requested_at))

    @property
    def db_session(self) -> Session:
        return Session(self.db_engine)

    @staticmethod
    def _build_query_search(search: SearchQuery) -> Select:
        stmt = select(NLPModelDBModel)
        for field in search.__exact_match_fields__:
            if getattr(search, field):
                stmt = stmt.where(getattr(NLPModelDBModel, field) == getattr(search, field))
        if search.date_from:
            stmt = stmt.where(NLPModelDBModel.requested_at > search.date_from)
        if search.date_to:
            stmt = stmt.where(NLPModelDBModel.requested_at <= search.date_to + timedelta(hours=24))
        return stmt

    def _get_request_from_db(self, request_id: str) -> NLPModelDBModel:
        with self.db_session as session:
            request = session.query(NLPModelDBModel).get(request_id)
            if not request:
                raise RequestDoesNotExist(f"NLP request with id {request_id} does not exist")
            else:
                return request

    def update_request_status(self, request_id: str, status: str) -> NLPModel:
        with self.db_session as session:
            try:
                request = self._get_request_from_db(request_id=request_id)
                if request:
                    request.status = status
                    session.add(request)
                    session.commit()
                    return model_from_orm(request)
                else:
                    raise RequestDoesNotExist(f"No request with id {request_id} found.")
            except SQLAlchemyError as exc:
                logger.exception(exc)
                session.rollback()
                raise CriticalDBError(f"Failed to update {request_id} with status {status}")

    def update_request_results(self, request_id: str, results: List[str]) -> NLPModel:
        with self.db_session as session:
            try:
                request = self._get_request_from_db(request_id=request_id)
                if request:
                    request.results = results
                    session.add(request)
                    session.commit()
                    return model_from_orm(request)
                else:
                    raise RequestDoesNotExist(f"No request with id {request_id} found.")
            except SQLAlchemyError as exc:
                logger.exception(exc)
                session.rollback()
                raise CriticalDBError(f"Failed to update {request_id} with results {len(results)}")


class BaseController(Controller):
    def __init__(self, db_engine: Engine, ml_pipeline: MLPipeline):
        super().__init__(db_engine)
        self.ml_pipeline = ml_pipeline

    def predict(self, request: NLPRequest):
        req = self.create(request)
        logger.info(f"Store request {req} to the db")
        try:
            logger.info(f"Start ML Pipeline for id {req.id}")

            pred = self.ml_pipeline.pipeline(req.sentence)

            self.update_request_results(req.id, pred)
            self.update_request_status(req.id, "COMPLETED")
        except Exception as e:
            self.update_request_status(req.id, "FAILED")
            logger.error(e)
        finally:
            request = model_from_orm(self._get_request_from_db(req.id))
            logger.info(f"Finish ML Pipeline for id {request.id} with status {request.status}")
            return request

    def create(self, request: NLPRequest) -> NLPModel:
        """
        :param request: A NLPRequest instance with the essential request parameters.
        :return: A NLPModel instance with the request execution info.
        """

        # build request execution info
        request = NLPModel(
            status=Status.SUBMITTED.value,
            results=[],
            **request.dict()
        )
        request_ = model_to_orm(request)

        # store request in db
        with self.db_session as session:
            try:
                session.add(request_)
                session.commit()
                request = model_from_orm(request_)
            except SQLAlchemyError as e:
                logger.error(e)
                session.rollback()
                raise UnexpectedDBError(e)

        return request
