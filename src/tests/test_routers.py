import http

import pytest
from httpx import AsyncClient


@pytest.mark.anyio
class TestRouters:
    """Test the API routers."""

    async def test_health_check(self, client: AsyncClient) -> None:
        """Test the health check endpoint."""
        response = await client.get("v1/ht/")
        assert response.status_code == http.HTTPStatus.OK
        assert response.json() == {"status": "UP"}

    async def test_docs(self, client: AsyncClient) -> None:
        """Test the docs redirect endpoint."""
        response = await client.get("/docs")
        assert response.status_code == http.HTTPStatus.OK
        assert "Swagger UI" in response.text

    async def test_openapi_schema(self, client: AsyncClient) -> None:
        """Test the OpenAPI schema endpoint."""
        response = await client.get("v1/openapi.json")
        assert response.status_code == http.HTTPStatus.OK
        schema = response.json()
        assert schema["openapi"] == "3.1.0"
        assert "paths" in schema
        assert "/v1/ht/" in schema["paths"]
        assert "/v1/film/" in schema["paths"]
        assert "/v1/character/" in schema["paths"]
        assert "/v1/starship/" in schema["paths"]
