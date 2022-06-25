from __future__ import annotations

from typing import TypeVar, cast

from aiohttp import ClientSession

from ._mixin import CurrentUserMixin

__all__ = ["GitHubSession"]

T = TypeVar("T", bound=ClientSession)


class GitHubSession(ClientSession, CurrentUserMixin):
    async def __aenter__(self: T) -> T:
        return cast(T, await super().__aenter__())
