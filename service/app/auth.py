import datetime
import logging
import os

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import DecodeError, ExpiredSignatureError, decode
from jwt import encode


class APIConfig:
    jwt_secret = os.getenv('JWT_SECRET', 'test')
    jwt_algorithm = os.getenv('JWT_ALGORITHM', 'HS256')


class JWTBearer(HTTPBearer):
    def __init__(
            self,
            jwt_secret: str,
            jwt_algorithm: str,
            auto_error: bool = True
    ):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self._jwt_secret = jwt_secret
        self._jwt_algorithm = jwt_algorithm

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")

            if self.decode_jwt(credentials.credentials):
                return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def decode_jwt(self, jwt_token: str):
        try:
            return decode(jwt_token, self._jwt_secret, algorithms=[self._jwt_algorithm])
        except DecodeError:
            raise HTTPException(403, 'Invalid authorization parameters')
        except ExpiredSignatureError:
            raise HTTPException(403, 'Expired token')


LOGGER = logging.getLogger(__name__)


class JWTFactory:
    """
    Factory object for JWT tokens.
    """
    REGISTERED_CLAIMS = frozenset(['exp', 'nbf', 'iss', 'aud', 'iat'])

    def __init__(self, secret, algorithm='HS256', duration=3600):
        """
        Creates a new JWT factory.
        :param secret: the secret to use for generating the tokens.
        :param algorithm: algorithm to use for encrypting the tokens.
        :param duration: number of seconds from now after which the token will expire.
        """
        self._secret = secret
        self._algorithm = algorithm
        self._duration = duration

    def create_token(self, extra_fields=None):
        """
        Generates the Auth Token.
        :param extra_fields: extra fields to add to JWT payload. If any key tries to override registered claim names,
                            it will be ignored. See
                            https://pyjwt.readthedocs.io/en/latest/usage.html#registered-claim-names for registered
                            claim names.
        :return: string the token.
        """
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=self._duration),
            'iat': datetime.datetime.utcnow(),
            'alg': self._algorithm
        }

        if isinstance(extra_fields, dict):
            payload.update(dict((k, v) for k, v in extra_fields.items() if k not in self.REGISTERED_CLAIMS))

        return encode(payload, self._secret, algorithm=self._algorithm)


def create_jwt_bearer() -> JWTBearer:
    config = APIConfig()
    return JWTBearer(jwt_secret=config.jwt_secret, jwt_algorithm=config.jwt_algorithm)
