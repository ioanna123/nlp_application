from uuid import uuid4

from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy import func
from sqlalchemy.orm import declarative_base

from service.data_model.status import Status

Base = declarative_base()


class NLPModelDBModel(Base):
    __tablename__ = 'nlp_table'
    __fields__ = [
        'id', 'client', 'sentence', 'requested_at',
        'updated', 'status', 'ml_metadata', 'results'

    ]

    id = Column(String, primary_key=True, default=lambda: uuid4().hex)
    sentence = Column(String, nullable=False)
    requested_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    status = Column(String, nullable=False, default=Status.SUBMITTED.value)
    client = Column(String, nullable=False)
    results = Column(JSON, nullable=False, default=[])
