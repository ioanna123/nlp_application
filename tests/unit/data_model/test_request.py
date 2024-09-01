import datetime
import unittest

from pydantic import ValidationError

from service.data_model.request import NLPRequest, NLPModel, model_from_orm, model_to_orm
from service.db.schema import NLPModelDBModel


class DataModelTestCase(unittest.TestCase):

    def test_normal_payloads(self):
        request = NLPRequest(
            sentence="lala <blank>",
            client="client",
        )
        self.assertListEqual(
            sorted(list(request.dict().keys())),
            sorted(["client", "sentence"])
        )

    def test_missing_required_fields(self):
        with self.assertRaises(ValidationError):
            NLPRequest(
                sentence="lala <blank>"
            )

    def test_incorrect_input(self):
        with self.assertRaises(ValidationError):
            request = NLPRequest(
                sentence="lala",
                client="client",
            )
        with self.assertRaises(ValidationError):
            request = NLPRequest(
                sentence="",
                client="client",
            )
        with self.assertRaises(ValidationError):
            request = NLPRequest(
                sentence="lal ala la <blank> lalalala, alalal, alaa!? lalal al lala lala, lala",
                client="client",
            )
        with self.assertRaises(ValidationError):
            request = NLPRequest(
                sentence="λαλλα <blank>",
                client="client",
            )

    def test_metadata_happy_path(self):
        m = NLPModel(
            id="hkwedkyuwge",
            sentence="lalal <blank>",
            client="client",
            requested_at=datetime.datetime(2022, 2, 2, 2, 2, 2),
            updated=datetime.datetime(2022, 2, 2, 2, 2, 4),
            status="RUNNING",
            results=[]
        )

        self.assertEqual(len(m.dict()), 7)
        self.assertEqual(m.client, "client")
        self.assertEqual(m.status, "RUNNING")


class AdaptersDataModelTestCase(unittest.TestCase):

    def test_model_to_orm_happy_request(self):
        request = NLPModel(
            id="hkwedkyuwge",
            sentence="lalal <blank>",
            client="client",
            requested_at=datetime.datetime(2022, 2, 2, 2, 2, 2),
            updated=datetime.datetime(2022, 2, 2, 2, 2, 4),
            status="RUNNING",
            results=[]
        )
        request_model = model_to_orm(request)
        self.assertIsNotNone(request_model)
        self.assertIsInstance(request_model, NLPModelDBModel)

    def test_from_orm_happy_request(self):
        request = NLPModelDBModel(
            id="hkwedkyuwge",
            sentence="lalal <blank>",
            client="client",
            requested_at=datetime.datetime(2022, 2, 2, 2, 2, 2),
            updated=datetime.datetime(2022, 2, 2, 2, 2, 4),
            status="RUNNING",
            results=[]
        )
        request_model = model_from_orm(request)
        self.assertIsNotNone(request_model)
        self.assertIsInstance(request_model, NLPModel)
