from datetime import datetime, timezone, timedelta

from jwt import encode


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
            'exp': datetime.now(tz=timezone.utc) + timedelta(days=0, seconds=self._duration),
            'iat': datetime.now(tz=timezone.utc),
            'alg': self._algorithm
        }

        if isinstance(extra_fields, dict):
            payload.update(dict((k, v) for k, v in extra_fields.items() if k not in self.REGISTERED_CLAIMS))

        return encode(payload, self._secret, algorithm=self._algorithm)
