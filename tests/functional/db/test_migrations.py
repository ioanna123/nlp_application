import os
import unittest
from unittest import mock

import pytest
from sqlalchemy.orm import declarative_base, Session
from alembic import command
from alembic.config import Config
from sqlalchemy import inspect, create_engine, Column, String, select

Base = declarative_base()


class AlembicMigrationsDBModel(Base):
    __tablename__ = 'alembic_version'
    __fields__ = ['version_num']

    version_num = Column(String, primary_key=True, )


@mock.patch.dict(
    os.environ,
    {
        "PSQL_CONN_URL": "postgresql://postgres:postgres@localhost:5432/postgres"
    },
    clear=True
)
@mock.patch('service.utils.logs.initialize_logging', mock.Mock())
class RunMigrationsUpgradeTestCase(unittest.TestCase):
    alembic_cfg = Config()
    alembic_cfg.set_main_option('script_location', 'alembic/')

    def setUp(self):
        self.engine = create_engine(f"postgresql+psycopg2://postgres:postgres@localhost:5432/postgres")
        self.inspector = inspect(self.engine)
        self.db_session = Session(self.engine)

    @pytest.mark.order(1)
    @mock.patch('service.db.factories.create_db_engine')
    def test_alembic_run_initial_migration_creates_tables_ok(self, mock_engine):
        # arrange
        mock_engine.return_value = self.engine
        # act
        command.upgrade(config=self.alembic_cfg, revision='ec1ee9')

        # assert migrations exist
        with self.db_session as session:
            revision = session.execute(select(AlembicMigrationsDBModel)).first()
        tables = self.inspector.get_table_names()

        table_columns = [
            column.get('name') for column in self.inspector.get_columns('nlp_table')
        ]
        table_columns_on_first_migration = [
            'id', 'sentence', 'updated', 'client',
            'requested_at', 'results', 'status',
        ]
        self.assertEqual(revision[0].version_num, 'ec1ee9')
        self.assertListEqual(sorted(tables), sorted(['alembic_version', 'nlp_table']))
        self.assertListEqual(
            sorted(table_columns),
            sorted(table_columns_on_first_migration)
        )
