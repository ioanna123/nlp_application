from datetime import date
from unittest import TestCase

from pydantic.error_wrappers import ValidationError

from service.data_model.request import search_params_to_data_model, SearchQuery
from service.data_model.status import Status


class TestQueryDataModel(TestCase):

    def test_search_params_to_data_model_happy_request(self):
        # act
        request_model = search_params_to_data_model(
            status='SUBMITTED',
            client='a_key',
            date_from='2020-01-01',
            date_to='2022-01-01'
        )

        # assert
        self.assertIsNotNone(request_model)
        self.assertEqual(request_model.status, Status.SUBMITTED.value)
        self.assertIsInstance(request_model.date_to, date)
        self.assertIsInstance(request_model.date_from, date)
        self.assertIsInstance(request_model, SearchQuery)

    def test_search_params_to_data_model_missing_values(self):
        # act
        request_model = search_params_to_data_model(
            status=None,
            client='client',
            date_from='2020-01-01',
            date_to='2022-01-01'
        )

        # assert
        self.assertIsNotNone(request_model)
        self.assertIsNone(request_model.status)
        self.assertIsInstance(request_model.date_to, date)
        self.assertIsInstance(request_model.date_from, date)
        self.assertIsInstance(request_model, SearchQuery)

        # act
        request_model = search_params_to_data_model(
            status="SUBMITTED",
            client='a_client',
            date_from=None,
            date_to='2022-01-01'
        )

        # assert
        self.assertIsNotNone(request_model)
        self.assertEqual(request_model.status, Status.SUBMITTED.value)
        self.assertEqual(request_model.status, Status.SUBMITTED.value)
        self.assertIsInstance(request_model.date_to, date)
        self.assertIsNone(request_model.date_from)
        self.assertIsInstance(request_model, SearchQuery)

    def test_search_params_to_data_model_status_validationError(self):
        with self.assertRaises(ValidationError):
            search_params_to_data_model(
                status='submitted',
                date_from='2020-01-01',
                date_to='2022-01-01',
                client='client',
            )

    def test_search_params_to_data_model_date_validationError(self):
        with self.assertRaises(ValidationError):
            search_params_to_data_model(
                status='SUBMITTED',
                client='client',
                date_from='2020/01/01',
                date_to='2022-01-01'
            )
            search_params_to_data_model(
                status='SUBMITTED',
                client='client',
                date_from='2020-01-01',
                date_to='2022/01/01'
            )
