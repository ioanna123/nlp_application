import datetime
from unittest import TestCase

import mock
import testing.postgresql
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from service.controller.controller import BaseController
from service.controller.errors import RequestDoesNotExist, CriticalDBError
from service.data_model.request import NLPRequest
from service.data_model.status import Status
from service.db.errors import UnexpectedDBError
from service.db.factories import create_db_tables
from service.db.schema import NLPModelDBModel


class MLPipelineMock:
    def pipeline(self, sentence):
        return ["good, nice"]


request_model = NLPModelDBModel(
    id="hkwedkyuwge",
    sentence="lalal <blank>",
    client="client",
    requested_at=datetime.datetime(2022, 2, 2, 2, 2, 2),
    updated=datetime.datetime(2022, 2, 2, 2, 2, 4),
    status="RUNNING",
    results=[]
)
request = NLPRequest(sentence='hshs <blank>', client='test')


def _add_to_db(request, session):
    session.add(request)
    session.commit()


class TestBaseControllerRetrieve(TestCase):
    def setUp(self):
        self.postgresql = testing.postgresql.Postgresql()
        self.engine = create_engine(self.postgresql.url())
        self.session = Session(self.engine)
        pipeline = MLPipelineMock()
        create_db_tables(self.engine)
        self.base_controller = BaseController(db_engine=self.engine, ml_pipeline=pipeline)

    def tearDown(self):
        self.postgresql.stop()

    def test_retrieve_request_none_exception(self):
        with self.assertRaises(RequestDoesNotExist):
            self.base_controller.retrieve('test_id')

    def test_retrieve_request_invalid_id(self):
        _add_to_db(request=request_model, session=Session(self.engine))
        with self.assertRaises(RequestDoesNotExist):
            self.base_controller.retrieve("test")


class TestBaseControllerCreate(TestCase):
    def setUp(self):
        self.postgresql = testing.postgresql.Postgresql()
        self.engine = create_engine(self.postgresql.url())
        self.session = Session(self.engine)
        pipeline = MLPipelineMock()
        create_db_tables(self.engine)
        self.base_controller = BaseController(db_engine=self.engine, ml_pipeline=pipeline)

    def tearDown(self):
        self.postgresql.stop()

    @mock.patch('service.controller.controller.Session.add')
    def test_create_request_raise_sql_alchemy_error(self, mock_session):
        mock_session.side_effect = SQLAlchemyError
        with self.assertRaises(UnexpectedDBError):
            self.base_controller.create(request)

    def test_create_request_none_input_exception(self):
        with self.assertRaises(Exception):
            self.base_controller.create(None)

    def test_create_request_ok(self):
        response = self.base_controller.create(request)

        self.assertListEqual(response.results, [])
        self.assertIsNotNone(response.id)
        self.assertIsNotNone(response.requested_at)
        self.assertEqual(response.status, Status.SUBMITTED.value)
        self.assertEqual(response.sentence, request.sentence)
        self.assertEqual(response.client, request.client)


class TestBaseControllerPredict(TestCase):
    def setUp(self):
        self.postgresql = testing.postgresql.Postgresql()
        self.engine = create_engine(self.postgresql.url())
        self.session = Session(self.engine)
        pipeline = MLPipelineMock()
        create_db_tables(self.engine)
        self.base_controller = BaseController(db_engine=self.engine, ml_pipeline=pipeline)

    def tearDown(self):
        self.postgresql.stop()

    @mock.patch('service.controller.controller.Session.add')
    def test_predict_request_raise_sql_alchemy_error(self, mock_session):
        mock_session.side_effect = SQLAlchemyError
        with self.assertRaises(UnexpectedDBError):
            self.base_controller.predict(request)

    def test_predict_request_none_input_exception(self):
        with self.assertRaises(Exception):
            self.base_controller.predict(None)


class TestControllerUpdate(TestCase):
    def setUp(self):
        self.postgresql = testing.postgresql.Postgresql()
        self.engine = create_engine(self.postgresql.url())
        self.session = Session(self.engine)
        pipeline = MLPipelineMock()
        create_db_tables(self.engine)
        self.base_controller = BaseController(db_engine=self.engine, ml_pipeline=pipeline)

    def tearDown(self):
        self.postgresql.stop()

    def test_update_request_raise_exception(self):
        with self.assertRaises(RequestDoesNotExist):
            self.base_controller.update_request_status(request_id="test",
                                                       status="RUNNING")

    @mock.patch('service.controller.controller.Session.query')
    def test_update_request_raise_sql_exception(self, mock_session):
        mock_session.side_effect = SQLAlchemyError
        with self.assertRaises(CriticalDBError):
            self.base_controller.update_request_status(
                request_id="test", status="RUNNING")
