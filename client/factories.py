from typing import Any, Dict

from client.client import DEFAULT_TIMEOUT, Client
from client.jwt_factory import JWTFactory


def create_client(
        base_url: str,
        jwt_secret: str,
        header: Dict[str, Any] = None,
        verify: bool = False,
        timeout: int = DEFAULT_TIMEOUT,
) -> Client:
    """
    Factory to generate a client.
    :param base_url: The API base url.
    :param jwt_secret: The JWT secret for jwt authentication.
    :param header: The header (optional) for the requests.
    :param verify: Verify SSL param.
    :param timeout: The request timeout.
    :return: A service instance.
    """

    base_header = {
        "ContentType": "application/json",
        "Accept": "application/json",
    }
    if header:
        base_header.update(header)

    return Client(
        headers=base_header,
        base_url=base_url,
        timeout=timeout,
        verify=verify,
        jwt=JWTFactory(secret=jwt_secret),
    )
