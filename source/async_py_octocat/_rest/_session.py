from __future__ import annotations

from types import TracebackType
from typing import Any, Type

from aiohttp import ClientSession

from ._mixin import RepoAccessMixin, UserAccessMixin

__all__ = ["GitHubSession"]


class GitHubSession(UserAccessMixin, RepoAccessMixin):

    session: ClientSession

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.session = ClientSession(*args, **kwargs)

    async def __aenter__(self) -> GitHubSession:
        await self.session.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType,
    ) -> None:
        return await self.session.__aexit__(exc_type, exc_val, exc_tb)
