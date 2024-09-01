from alembic import context

from service.db.schema import Base
from service.db.factories import create_db_engine
from service.utils.logs import initialize_logging

initialize_logging('config/logging.yaml')

config = context.config
target_metadata = Base.metadata


def run_migrations_online():
    engine = create_db_engine()

    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
