import logging
from typing import Any, Literal, Mapping, MutableMapping, MutableSequence

import aiohttp
from yarl import URL

logger = logging.getLogger(__name__)


class Plugin:
    """Base class for plugins to interact with external APIs."""

    API_TIMEOUT: int = 10  # seconds
    auth: aiohttp.BasicAuth | None = None

    BASE_URL: str

    def _base_url(self) -> URL:
        """Construct the base URL for the API."""
        return URL(self.BASE_URL)

    async def _get(
        self,
        url: str | URL,
        params: Mapping[str, str] | None = None,
        headers: MutableMapping[str, str] | None = None,
    ) -> dict:
        """Wrapper for making GET requests."""
        return await self._http("GET", url, params=params, headers=headers)

    async def _http(
        self,
        action: Literal["GET", "POST", "PUT", "PATCH", "DELETE"],
        url: str,
        params: Mapping[str, str] | None = None,
        headers: MutableMapping[str, str] | None = None,
        json: MutableSequence[Any] | Mapping[str, Any] | None = None,
        data: Mapping[str, str] | None = None,
    ) -> dict:
        """Wrapper for making HTTP requests."""
        kwargs: dict[str, Any] = {
            "timeout": self.API_TIMEOUT,
            "headers": headers,
            "json": json,
            "data": data,
            "params": params,
            "auth": self.auth,
        }

        # Construct url
        url = self._base_url().join(URL(url))
        logger.debug(
            "Making %s request to %s with params: %s, headers: %s, json: %s",
            action,
            url,
            params,
            headers,
            json,
        )

        async with aiohttp.ClientSession() as session:
            async with session.request(method=action, url=url, **kwargs) as response:
                response.raise_for_status()
                return await response.json()
