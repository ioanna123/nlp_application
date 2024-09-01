import factory
from factory import fuzzy

from service.data_model.request import NLPRequest, NLPModel, SearchQuery
from service.data_model.status import Status


class NLPRequestFactory(factory.Factory):
    class Meta:
        model = NLPRequest
    sentence = "lalalala <blank>"
    client = factory.Faker('text', max_nb_chars=10)


class NLPModelFactory(NLPRequestFactory):
    class Meta:
        model = NLPModel

    id = factory.Faker('text', max_nb_chars=35)
    status = fuzzy.FuzzyChoice([status.value for status in Status])
    results = []


class SearchQueryFactory(factory.Factory):
    class Meta:
        model = SearchQuery

    status = fuzzy.FuzzyChoice([status.value for status in Status])
