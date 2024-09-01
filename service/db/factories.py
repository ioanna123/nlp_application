from sqlalchemy.engine import create_engine, Engine

from service.db.config import PSQLConfig, psql_config
from service.db.schema import Base


def create_db_tables(engine: Engine):
    """
    Creates all tables under the schema module (if missing).
    :param engine: The SQLAlchemy engine.
    """

    Base.metadata.create_all(engine)


def drop_db_tables(engine: Engine):
    Base.metadata.drop_all(engine)


def create_db_engine(config: PSQLConfig = None) -> Engine:
    """
    Factory method for the database engine. Creates an SQLAlchemy Engine from the database configuration.
    :return: The generated engine.
    """
    config = config or psql_config()
    engine = create_engine(config.psql_conn_url, pool_pre_ping=True)
    # create_db_tables(engine=engine)
    return engine
