import re
from datetime import datetime, date
from typing import List, Optional

from pydantic import BaseModel, validator

from service.data_model.status import Status
from service.db.schema import NLPModelDBModel


class MLMetadata(BaseModel):
    init_suggestions: List[str]
    sent_anal_suggestion: List[str]


class UpdateRequestModel(BaseModel):
    status: Optional[str]
    ml_metadata: Optional[MLMetadata]
    results: Optional[List[str]]


class NLPRequest(BaseModel):
    """
    Pydantic dataclass representing the request payload.
    """

    __writeable_fields__ = [
        'sentence', 'client',
    ]

    sentence: str
    client: str

    @validator('sentence')
    def validate_sentence(cls, value):
        # Check for the presence of <blank>
        if '<blank>' not in value:
            raise ValueError("Sentence must contain a '<blank>' placeholder.")

        # Check if the sentence is between 1 and 10 words
        word_count = len(re.findall(r'\b\w+\b', value))
        if word_count < 1 or word_count > 10:
            raise ValueError("Sentence must be between 1 and 10 words.")

        # Check if the sentence is in English (simple heuristic check)
        if not all(ord(char) < 128 for char in value):
            raise ValueError("Sentence must contain only English characters.")

        # Check for special characters, allow only specified ones
        if re.search(r'[^\w\s<>,.!?]', value):
            raise ValueError("Sentence contains invalid special characters.")

        return value


class NLPModel(NLPRequest):
    """
    Pydantic dataclass representing the info payload.
    """

    __writeable_fields__ = ['status', 'results'] + NLPRequest.__writeable_fields__

    id: Optional[str] = None
    status: Status
    requested_at: Optional[datetime] = None
    updated: Optional[datetime] = None
    results: List[str]

    class Config:
        use_enum_values = True
        from_attributes = True


def model_to_orm(model: NLPModel) -> NLPModelDBModel:
    data = {k: v for k, v in model.dict().items() if k in model.__writeable_fields__}
    return NLPModelDBModel(**data)


def model_from_orm(dbmodel: NLPModelDBModel) -> NLPModel:
    return NLPModel.from_orm(dbmodel)


class SearchQuery(BaseModel, use_enum_values=True):
    """
    Pydantic dataclass representing the search query.
    """

    __exact_match_fields__ = ['status', 'client']

    status: Optional[Status] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    client: Optional[str] = None


def search_params_to_data_model(
        status: Status,
        client: str,
        date_from: str,
        date_to: str) -> SearchQuery:
    return SearchQuery(**
                       {
                           'status': status,
                           'client': client,
                           'date_to': date_to,
                           'date_from': date_from
                       })
