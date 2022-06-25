from __future__ import annotations

from typing import Optional

from aiohttp import ClientSession

from .._constants import BASE_URL
from .._models import User
from ..exceptions import (
    Forbidden403,
    NotModified304,
    RequiresAuthentication401,
)

__all__ = ["UserAccessMixin"]


class UserAccessMixin:

    session: ClientSession

    async def get_user(self, username: Optional[str] = None) -> User:
        if username is None:
            return await self._get_user(f"{BASE_URL}/user")
        else:
            return await self._get_user(f"{BASE_URL}/users/{username}")

    async def _get_user(self, url: str) -> User:
        async with self.session.get(url) as response:
            content = await response.text()
            if response.status == 401:
                raise RequiresAuthentication401(content)
            if response.status == 304:
                raise NotModified304(content)
            if response.status == 403:
                raise Forbidden403(content)
            assert response.status == 200, response
        user = User.parse_raw(content, content_type="json")
        user._session = self  # type: ignore
        return user
