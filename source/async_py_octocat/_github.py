from __future__ import annotations

from typing import Any, Generator, Optional

import aiohttp

from ._rest import GitHubSession, User


class GitHub:
    """Async GitHub client.

    After instantiation this object should (but doesn't have to) be
    awaited to verify credentials and download authenticated user
    profile data. Awaiting this object return self (this client object).
    """

    username: str
    token: str
    token_auth: bool
    _user: Optional[User]

    def __init__(
        self, username: str, token: str, token_auth: bool = False
    ) -> None:
        self.username = username
        self.token = token
        self.token_auth = token_auth
        self._user = None

    def __await__(self) -> Generator[Any, None, GitHub]:
        """Verifies credentials by downloading authenticated user profile data.

        Returns
        -------
        Coroutine[Any, Any, GitHub]
            self
        """
        return self._fetch_current_user().__await__()  # type: ignore

    async def _fetch_current_user(self) -> GitHub:
        async with self._session as session:
            self._user = await session.get_user()
        return self

    @property
    def _session(self) -> GitHubSession:
        if self.token_auth:
            return GitHubSession(
                headers={
                    "Accept": "application/vnd.github.v3+json",
                    "Authorization": f"token {self.token}",
                },
            )
        else:
            return GitHubSession(
                auth=aiohttp.BasicAuth(
                    login=self.username, password=self.token
                ),
                headers={"Accept": "application/vnd.github.v3+json"},
            )

    async def user(self, username: Optional[str] = None) -> User:
        if username is None:
            if self._user is None:
                await self._fetch_current_user()
            assert self._user is not None
            return self._user
        else:
            async with self._session as session:
                user = await session.get_user(username)
            return user
