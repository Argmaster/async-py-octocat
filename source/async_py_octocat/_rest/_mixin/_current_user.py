from __future__ import annotations

from typing import Any

import aiohttp

from .._models import User


class CurrentUserMixin:
    def get(
        self, url: str, *args: Any, **kwargs: Any
    ) -> aiohttp.ClientResponse:
        ...  # pragma: no cover

    async def get_current_user(self) -> User:
        async with self.get("https://api.github.com/user") as response:
            print(response.status)
            content = await response.text()
        return User.parse_raw(content, content_type="json")
