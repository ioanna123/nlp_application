import aiounittest

from unittest.mock import MagicMock
from fastapi import HTTPException

from service.app.auth import JWTBearer, JWTFactory


class JWTBearerTestCase(aiounittest.AsyncTestCase):

    async def test_happy_path(self):
        bearer = JWTBearer(jwt_secret="secret", jwt_algorithm="HS256")

        jwt = JWTFactory(secret="secret")
        token = jwt.create_token()

        result = await bearer(request=MagicMock(headers={'Authorization': f"Bearer {token}"}))
        self.assertEqual(result, token)

    async def test_invalid_scheme(self):
        bearer = JWTBearer(jwt_secret="secret", jwt_algorithm="HS256")
        with self.assertRaises(HTTPException):
            await bearer(request=MagicMock(headers={'Authorization': 'token'}))

    async def test_invalid_token(self):
        bearer = JWTBearer(jwt_secret="secret", jwt_algorithm="HS256")
        with self.assertRaises(HTTPException):
            await bearer(request=MagicMock(headers={'Authorization': 'Bearer token'}))
