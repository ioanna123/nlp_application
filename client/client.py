import logging
from typing import Dict, Any

import requests
from requests import codes, Response

from client.data_model import NLPRequest, NLPModel
from client.jwt_factory import JWTFactory

DEFAULT_TIMEOUT = 60

logger = logging.getLogger(__name__)


class Client:
    endpoint = "/request"

    def __init__(
            self,
            base_url: str,
            jwt: JWTFactory,
            headers: Dict,
            verify=False,
            timeout=DEFAULT_TIMEOUT,
    ):
        self._jwt_factory = jwt
        self.headers = headers
        self.base_url = base_url
        self.verify = verify
        self.timeout = timeout
        self._session = requests.Session()

    def _request(self, **kwargs: Any) -> Response:
        """
        Perform a request using requests methods.

        :param kwargs: parameters of the request
        :return: response from request sent
        :rtype: requests.Response
        """
        # check key word args contain accepted codes
        # if yes parse it and delete it from kwargs t
        accepted_codes = [requests.codes.ok]
        if "accepted_codes" in kwargs:
            accepted_codes = kwargs.pop("accepted_codes")

        timeout = self.timeout
        if "timeout" in kwargs:
            timeout = kwargs.pop("timeout")

        url = self.base_url + kwargs.pop("url")
        updated_headers = self.headers
        updated_headers.update(kwargs.get("headers", {}))
        self.headers = updated_headers

        try:
            response = self._session.request(
                headers=self.headers,
                url=url,
                verify=self.verify,
                timeout=timeout,
                **kwargs,
            )
        except Exception as e:
            logger.error(str(e))
            raise e

        if response.status_code not in accepted_codes:
            logger.error(f"{response.status_code} not in {accepted_codes}")
        return response

    def _refresh_token(self):
        # inject authorization fields
        token = self._jwt_factory.create_token()
        token = token.decode() if isinstance(token, bytes) else token
        self.headers["Authorization"] = f"Bearer {token}"

    def create_request(self, request: NLPRequest) -> NLPModel:
        """
        Request to create a request

        :param request: A Request instance containing vital request data.
        :return: An instance containing request metadata (id, status, etc.).
        """
        self._refresh_token()
        response = self._request(
            url=self.endpoint,
            method="POST",
            json=request.dict(),
            accepted_codes=[codes.ok, codes.created, codes.accepted],
        )

        return NLPModel(**response.json())

    def retrieve_request(self, request_id: str) -> NLPModel:
        """
        Request to retrieve information regarding a request.

        :param request_id: The ID of the pair-matching request id.
        :return: An instance containing request metadata (id, status, etc.).
        """

        self._refresh_token()
        response = self._request(
            url=f"{self.endpoint}/{request_id}",
            method="GET",
            accepted_codes=[codes.ok],
        )
        return NLPModel(**response.json())
