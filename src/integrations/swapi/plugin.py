from src.integrations.api import Plugin


class SwapiPlugin(Plugin):
    """Plugin to interact with the Star Wars API (SWAPI)."""

    NAME = "swapi"
    BASE_URL = "https://swapi.info/api/"

    async def starships(self) -> list[dict]:
        """Fetch starships from the Star Wars API."""
        return await self._get("starships/")

    async def starship(self, id: int) -> dict:
        """Fetch a specific starship by ID from the Star Wars API."""
        return await self._get(f"starships/{id}/")

    async def characters(self) -> list[dict]:
        """Fetch people from the Star Wars API."""
        return await self._get("people/")

    async def character(self, id: int) -> dict:
        """Fetch a specific character by ID from the Star Wars API."""
        return await self._get(f"people/{id}/")

    async def films(self) -> list[dict]:
        """Fetch films from the Star Wars API."""
        return await self._get("films/")

    async def film(self, id: int) -> dict:
        """Fetch a specific film by ID from the Star Wars API."""
        return await self._get(f"films/{id}/")
