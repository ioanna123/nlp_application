from unittest import mock, TestCase
from unittest.mock import MagicMock

from ds_swe_commons.patterns.proxy import Proxy

from ds_metadata_linking.controller.controller import Controller
from ds_metadata_linking.controller.factory import create_controller, create_r2c_pair_controller, \
    create_r2r_pair_controller, create_c2c_pair_controller
from ds_metadata_linking.controller.pair_controller import R2CPairController, R2RPairController, C2CPairController


class FactoryTestCase(TestCase):
    @mock.patch('ds_metadata_linking.utils.datadog.factory.dd_metric_increase', MagicMock())
    @mock.patch('ds_metadata_linking.controller.factory.controller_config')
    @mock.patch('ds_metadata_linking.controller.factory.create_db_engine')
    @mock.patch('ds_metadata_linking.controller.factory.create_job_queue_producer')
    def test_create_controller(self, mock_prod, mock_db, mock_app):
        class Config:
            job_queue = 'job_queue'

        mock_app.return_value = Config()
        mock_db.return_value = MagicMock()
        mock_prod.return_value = MagicMock()
        controller = create_controller()
        self.assertIsInstance(controller, Controller)

    @mock.patch('ds_metadata_linking.controller.factory.create_controller')
    def test_create_proxy_controller(self, mock_prod):
        from ds_metadata_linking.controller.factory import proxy_controller
        mock_prod.return_value = MagicMock()
        proxy_controller = proxy_controller()
        self.assertIsInstance(proxy_controller, Proxy)

    @mock.patch('ds_metadata_linking.controller.factory.create_pairwise_config')
    @mock.patch('ds_metadata_linking.controller.factory.create_db_engine')
    @mock.patch('ds_metadata_linking.controller.factory.create_job_queue_producer')
    def test_create_r2c_pair_controller(self, mock_prod, mock_db, mock_app):
        class Config:
            r2c_pair_queue = 'r2c_pair_queue'

        mock_app.return_value = Config()
        mock_db.return_value = MagicMock()
        mock_prod.return_value = MagicMock()
        controller = create_r2c_pair_controller()
        self.assertIsInstance(controller, R2CPairController)

    @mock.patch('ds_metadata_linking.controller.factory.create_pairwise_config')
    @mock.patch('ds_metadata_linking.controller.factory.create_db_engine')
    @mock.patch('ds_metadata_linking.controller.factory.create_job_queue_producer')
    def test_create_r2r_pair_controller(self, mock_prod, mock_db, mock_app):
        class Config:
            r2r_pair_queue = 'r2r_pair_queue'

        mock_app.return_value = Config()
        mock_db.return_value = MagicMock()
        mock_prod.return_value = MagicMock()
        controller = create_r2r_pair_controller()
        self.assertIsInstance(controller, R2RPairController)

    @mock.patch('ds_metadata_linking.controller.factory.create_pairwise_config')
    @mock.patch('ds_metadata_linking.controller.factory.create_db_engine')
    @mock.patch('ds_metadata_linking.controller.factory.create_job_queue_producer')
    def test_create_c2c_pair_controller(self, mock_prod, mock_db, mock_app):
        class Config:
            c2c_pair_queue = 'c2c_pair_queue'

        mock_app.return_value = Config()
        mock_db.return_value = MagicMock()
        mock_prod.return_value = MagicMock()
        controller = create_c2c_pair_controller()
        self.assertIsInstance(controller, C2CPairController)
