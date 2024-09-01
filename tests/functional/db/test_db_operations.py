import unittest
from unittest import mock
from unittest.mock import MagicMock

from sqlalchemy import inspect, create_engine, Column, String, Table, JSON, DateTime, MetaData, func
from sqlalchemy.orm import Session

from service.controller.controller import BaseController
from service.data_model.request import NLPRequest, NLPModel
from service.data_model.status import Status
from service.db.factories import create_db_tables, drop_db_tables
from service.db.schema import NLPModelDBModel


@mock.patch('service.utils.logs.initialize_logging', mock.Mock())
class DBFunctionalTests(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/postgres")
        self.db_session = Session(self.engine)
        self.inspector = inspect(self.engine)

    def test_create_table_in_db_ok(self):
        # act
        create_db_tables(self.engine)

        tables = self.inspector.get_table_names()

        # assert
        self.assertGreater(len(tables), 0)

    def test_drop_all_tables_in_db_ok(self):
        # act
        drop_db_tables(self.engine)

        tables = self.inspector.get_table_names()

        # assert
        self.assertEqual(len(tables), 1)
        self.assertEqual(["alembic_version"], self.inspector.get_table_names())


@mock.patch('service.utils.logs.initialize_logging', mock.Mock())
class DBControllerFunctionalTests(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/postgres")
        self.db_session = Session(self.engine)
        meta = MetaData()
        self.service = Table('nlp_table', meta,
                             Column('id', String, primary_key=True),
                             Column('sentence', String, nullable=False),
                             Column('client', String, nullable=False),
                             Column('requested_at', DateTime, server_default=func.now(), nullable=False),
                             Column('updated', DateTime, server_default=func.now(),
                                    onupdate=func.now(), nullable=False),
                             Column('status', String, nullable=False, default=Status.SUBMITTED.value),
                             Column('results', JSON, nullable=False, default=[]),
                             )
        self.service.create(self.engine)

    def test_store_request_in_db_ok(self):
        # act
        controller = BaseController(db_engine=self.engine, ml_pipeline=MagicMock())
        nlp = NLPRequest(sentence='hshs <blank>', client='test')

        request = controller.create(nlp)

        # assert
        self.assertIsNotNone(request)
        self.assertIsInstance(request, NLPModel)
        self.assertEqual(request.sentence, 'hshs <blank>')
        self.assertEqual(request.client, 'test')
        self.assertEqual(request.status, Status.SUBMITTED.value)

    def test_store_request_in_db_raises_sqlalchemy_error(self):
        # arrange
        controller = BaseController(db_engine=self.engine, ml_pipeline=MagicMock())
        # act/assert
        with self.assertRaises(AttributeError):
            controller.create(None)

    def test_retrieve_request_ok(self):
        # act
        self.db_session.add(
            NLPModelDBModel(id='1', status=Status.SUBMITTED.value,
                            client='client', sentence='hshs <blank>',
                            results=[])
        )
        self.db_session.commit()

        controller = BaseController(db_engine=self.engine, ml_pipeline=MagicMock())

        request_prediction = controller.retrieve(request_id='1')

        # assert
        self.assertEqual(request_prediction.id, '1')
        self.assertEqual(request_prediction.client, 'client')
        self.assertEqual(request_prediction.status, Status.SUBMITTED.value)

    def test_update_request_status_ok_request(self):
        self.db_session.add(
            NLPModelDBModel(id='1', status=Status.SUBMITTED.value, client='client', sentence='hshs <blank>', results=[])
        )
        self.db_session.commit()

        # act
        controller = BaseController(db_engine=self.engine, ml_pipeline=MagicMock())

        request = controller.update_request_status(request_id='1', status="RUNNING")
        # assert
        self.assertIsNotNone(request)
        self.assertEqual(request.status, Status.RUNNING.value)

    def tearDown(self):
        self.service.drop(self.engine)
        self.db_session.close()
        self.engine.dispose()
