import logging
from uuid import uuid4

from alembic import op
from sqlalchemy import Column, String, JSON, DateTime, func
from sqlalchemy.engine import Connection

from service.data_model.status import Status
from service.db.factories import create_db_engine
from service.db.schema import Base

logger = logging.getLogger(__name__)

revision = 'ec1ee9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """
    If missing, creates the table.
    """

    engine = create_db_engine()

    with Connection(engine) as conn, conn.begin():
        if not conn.dialect.has_table(conn, 'nlp_table'):
            logger.info("Creating table nlp_table")
            op.create_table(
                'nlp_table',
                Column('id', String, primary_key=True, default=lambda: uuid4().hex),
                Column('sentence', String, nullable=False),
                Column('client', String, nullable=False),
                Column('requested_at', DateTime, server_default=func.now(), nullable=False),
                Column('updated', DateTime, server_default=func.now(), onupdate=func.now(), nullable=False),
                Column('status', String, nullable=False, default=Status.SUBMITTED.value),
                Column('results', JSON, nullable=False, default=[]),
                schema=Base.metadata.schema
            )
        else:
            logger.info("Table nlp_table exists, skipping creation...")


def downgrade():
    op.drop_table('nlp_table')
