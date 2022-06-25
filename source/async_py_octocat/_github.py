from __future__ import annotations

from types import TracebackType
from typing import Optional, Type

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
    _session: GitHubSession

    def __init__(
        self, username: str, token: str, token_auth: bool = False
    ) -> None:
        self.username = username
        self.token = token
        self.token_auth = token_auth
        self._user = None
        self._session = self._get_session()

    def _get_session(self) -> GitHubSession:
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

    async def __aenter__(self) -> GitHub:
        await self._session.__aenter__()
        await self._fetch_current_user()
        return self

    async def _fetch_current_user(self) -> None:
        self._user = await self._session.get_user()

    async def __aexit__(
        self,
        exc_type: Type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType,
    ) -> None:
        return await self._session.__aexit__(exc_type, exc_val, exc_tb)

    async def user(self, username: Optional[str] = None) -> User:
        if username is None:
            if self._user is None:
                await self._fetch_current_user()
            assert self._user is not None
            return self._user
        else:
            user = await self._session.get_user(username)
            return user
