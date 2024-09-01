from client.data_model import NLPRequest
from client.factories import create_client

client = create_client(
    base_url="http://0.0.0.0:8000/",
    jwt_secret="test"
)

job = NLPRequest(sentence='have a <blank> day', client='ioanna')
response = client.create_request(job)
print(response)
