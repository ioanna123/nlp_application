from alembic.config import Config
from alembic import command


def run_migrations():
    alembic_cfg = Config()
    alembic_cfg.set_main_option('script_location', 'alembic/')
    command.upgrade(alembic_cfg, 'head')
