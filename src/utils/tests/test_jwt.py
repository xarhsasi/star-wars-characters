from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from src.utils.jwt import JwtAuthenticationService, JwtHTTPBearer


@pytest.fixture
def mock_settings():
    class MockAuthConfig:
        JWT_SECRET_KEY = "testsecret"
        JWT_ALGORITHM = "HS256"
        JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 15

    class MockSettings:
        AUTH_CONFIG = MockAuthConfig()

    return MockSettings()


class TestJwtAuthenticationService:
    """Tests for JwtAuthenticationService."""

    @pytest.fixture(autouse=True)
    def setup(self, mock_settings):
        self.jwt_service = JwtAuthenticationService(settings=mock_settings)

    def test_encode_jwt(self):
        user_id = 123
        token = self.jwt_service.encode(user_id)
        assert isinstance(token, str)

    def test_verify_valid_jwt(self):
        user_id = 123
        token = self.jwt_service.encode(user_id)
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        payload = self.jwt_service.verify(credentials.credentials)
        assert payload["sub"] == str(user_id)

    def test_verify_invalid_jwt(self):
        invalid_token = "invalid.token.value"
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer", credentials=invalid_token
        )
        with pytest.raises(Exception):
            self.jwt_service.verify(credentials.credentials)


@pytest.mark.anyio
class TestJwtHTTPBearer:
    """Tests for JwtHTTPBearer."""

    @pytest.fixture(autouse=True)
    def setup(self, mock_settings):
        self.jwt_service = JwtAuthenticationService(settings=mock_settings)
        self.jwt_bearer = JwtHTTPBearer(auth_service=self.jwt_service)

    async def test_jwt_http_bearer_valid_token(self):
        user_id = 123
        token = self.jwt_service.encode(user_id)
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

        with patch("fastapi.security.HTTPBearer.__call__", return_value=credentials):
            result = await self.jwt_bearer.__call__(MagicMock())
            assert result == token

    async def test_jwt_http_bearer_invalid_scheme(self):
        credentials = HTTPAuthorizationCredentials(
            scheme="Basic", credentials="sometoken"
        )

        with patch("fastapi.security.HTTPBearer.__call__", return_value=credentials):
            with pytest.raises(HTTPException) as exc_info:
                await self.jwt_bearer.__call__(MagicMock())
            assert exc_info.value.status_code == 403
            assert exc_info.value.detail == "Invalid authentication scheme."

    async def test_jwt_http_bearer_no_credentials(self):
        with patch("fastapi.security.HTTPBearer.__call__", return_value=None):
            with pytest.raises(HTTPException) as exc_info:
                await self.jwt_bearer.__call__(MagicMock())
            assert exc_info.value.status_code == 403
            assert exc_info.value.detail == "Invalid authorization code."
