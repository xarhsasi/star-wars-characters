import abc
import http
import logging
from datetime import datetime
from typing import Final, Generic, TypeVar

import pytest
from httpx import AsyncClient
from sqlalchemy import inspect

logger = logging.getLogger(__name__)

_T = TypeVar("_T")  # ORM model type


@pytest.mark.anyio
class RouterTestBase(abc.ABC):
    """Base class for router integration tests."""

    MIN_ENTITIES: Final[int] = 10

    path: str  # Something like: "v1/entity/"
    entities: list[Generic[_T]]

    @pytest.fixture(autouse=True)
    @abc.abstractmethod
    async def setup(self):
        """Setup test data.
        This methos should be implemented in the subclass to create necessary test data.

        The base class expects self.entities to be set with a list of created entities with
        minimum {MIN_ENTITIES}.
        """

    async def test_setup(self) -> None:
        """Ensure setup created entities."""
        assert hasattr(self, "entities"), "setup() did not set self.entities"
        assert isinstance(self.entities, list), "self.entities is not a list"
        assert (
            len(self.entities) >= self.MIN_ENTITIES
        ), "self.entities has less than 10 items"


class RouterTestList(RouterTestBase):
    """Integration tests for listing entities in the router."""

    async def test_list_entities(self, client: AsyncClient) -> None:
        """Test listing entities."""
        response = await client.get(self.path)
        assert response.status_code == http.HTTPStatus.OK

        data = response.json()
        assert "items" in data
        assert "page" in data
        assert "page_size" in data
        assert "total" in data
        assert isinstance(data["items"], list)
        assert len(data["items"]) >= 10


class RouterTestRetrieve(RouterTestBase):
    """Integration tests for retrieving an entity by ID in the router."""

    async def test_retrieve_entity(self, client: AsyncClient) -> None:
        """Test retrieving an entity by ID."""
        entity = self.entities[0]
        entity_id = entity.id

        response = await client.get(f"{self.path}{entity_id}/")
        assert response.status_code == http.HTTPStatus.OK

        data = response.json()
        mapper = inspect(type(entity))  # mapper for the class (or: inspect(obj).mapper)
        column_names = {a.key for a in mapper.column_attrs}
        for key, value in data.items():
            assert key in column_names, f"Unexpected key in response: {key}"
            orm_val = getattr(entity, key)

            assert value == orm_val

    async def test_retrieve_entity_not_found(self, client: AsyncClient) -> None:
        """Test retrieving a non-existent entity."""
        response = await client.get(f"{self.path}999999999/")
        assert response.status_code == http.HTTPStatus.NOT_FOUND
        data = response.json()
        assert data["detail"] == "ORM model with ID 999999999 not found."


class RouterTestSearch(RouterTestBase):
    """Integration tests for searching entities by name in the router."""

    SEARCH_QUERY_ATTR: str  # Override in subclass if needed

    @property
    def _search_attr(self) -> str:
        """Get the attribute to search by."""
        search_attr = getattr(self.entities[0], self.SEARCH_QUERY_ATTR, None)
        if not search_attr:
            raise RuntimeError("SEARCH_QUERY_ATTR not set or invalid")
        return search_attr

    async def test_search_entities(self, client: AsyncClient) -> None:
        """Test searching for entities by name."""
        response = await client.get(
            f"{self.path}search/", params={"query": self._search_attr}
        )
        assert response.status_code == http.HTTPStatus.OK

        data = response.json()
        assert isinstance(data, list)
        assert any(ent[self.SEARCH_QUERY_ATTR] == self._search_attr for ent in data)

    async def test_search_entities_no_results(self, client: AsyncClient) -> None:
        """Test searching for entities with no matching results."""
        response = await client.get(
            f"{self.path}search/", params={"query": "NonExistentName"}
        )
        assert response.status_code == http.HTTPStatus.OK

        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    async def test_search_entities_case_insensitive(self, client: AsyncClient) -> None:
        """Test searching for entities by name in a case-insensitive manner."""
        entity_name = self._search_attr.lower()
        response = await client.get(
            f"{self.path}search/", params={"query": entity_name}
        )
        assert response.status_code == http.HTTPStatus.OK

        data = response.json()
        assert isinstance(data, list)
        assert any(ent[self.SEARCH_QUERY_ATTR].lower() == entity_name for ent in data)

    async def test_search_entities_partial_match(self, client: AsyncClient) -> None:
        """Test searching for entities by partial name match."""
        partial_name = self._search_attr[: len(self._search_attr) // 2]
        response = await client.get(
            f"{self.path}search/", params={"query": partial_name}
        )
        assert response.status_code == http.HTTPStatus.OK

        data = response.json()
        assert isinstance(data, list)
        assert any(partial_name in ent[self.SEARCH_QUERY_ATTR] for ent in data)

    async def test_search_entities_invalid_query(self, client: AsyncClient) -> None:
        """Test searching for entities with an invalid query parameter."""
        response = await client.get(f"{self.path}search/", params={"query": ""})
        assert response.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY
