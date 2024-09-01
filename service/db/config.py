import os


class PSQLConfig:
    """
    Configuration for the PostgreSQL DB connection.
    """
    psql_conn_url = os.getenv('PSQL_CONN_URL', 'postgresql://postgres:postgres@db:5432/postgres')


def psql_config() -> PSQLConfig:
    """
    Factory that creates the PSQLConfig instance.
    :return: A Postgres configuration object.
    """
    return PSQLConfig()
