from __future__ import annotations

from types import TracebackType
from typing import Any, Awaitable, Generator, Optional, Type

import aiohttp
from typing_extensions import Self

from ._rest import GitHubSession, User


class GitHub(Awaitable[Self]):
    """Async GitHub client.

    After instantiation this object should (but doesn't have to) be
    awaited to verify credentials and download authenticated user
    profile data. Awaiting this object return self (this client object).
    """

    username: str
    token: str
    user: Optional[User]

    def __init__(self, username: str, token: str) -> None:
        self.username = username
        self.token = token
        self.user = None

    def __await__(self) -> Generator[Any, None, GitHub]:
        """Verifies credentials by downloading authenticated user profile data.

        Returns
        -------
        Coroutine[Any, Any, GitHub]
            self
        """
        return self._check_credentials().__await__()  # type: ignore

    async def _check_credentials(self) -> GitHub:
        async with self._session as session:
            self.user = await session.get_current_user()
        return self

    @property
    def _session(self) -> GitHubSession:
        return GitHubSession(
            auth=aiohttp.BasicAuth(login=self.username, password=self.token)
        )

    def __aenter__(self) -> None:
        pass  # pragma: no cover

    def __aexit__(
        self,
        exc_type: Type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType,
    ) -> None:
        pass  # pragma: no cover
