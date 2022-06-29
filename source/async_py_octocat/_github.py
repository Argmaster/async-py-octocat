from __future__ import annotations

import hashlib
from random import random
from types import TracebackType
from typing import Optional, Type

from ._rest import GitHubSession, User

SESSION_ATTR_NAME: str = hashlib.sha256(
    str(random()).encode("utf-8")
).hexdigest()


class GitHub:
    """Async GitHub client.

    After instantiation this object should (but doesn't have to) be
    awaited to verify credentials and download authenticated user
    profile data. Awaiting this object return self (this client object).
    """

    username: str
    token: str
    is_token_auth: bool
    session: GitHubSession
    _user: Optional[User]

    def __init__(
        self, username: str, token: str, is_token_auth: bool = False
    ) -> None:
        self.username = username
        self.token = token
        self.is_token_auth = is_token_auth
        self._user = None
        self.session = GitHubSession(
            self.username, self.token, self.is_token_auth
        )

    async def __aenter__(self) -> GitHub:
        await self.session.__aenter__()
        self._user = await self.session.get_user()
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType,
    ) -> None:
        retval = await self.session.__aexit__(exc_type, exc_val, exc_tb)
        return retval

    async def user(self, username: Optional[str] = None) -> User:
        if username is None:
            if self._user is None:
                self._user = await self.session.get_user()
            assert self._user is not None
            return self._user
        else:
            user = await self.session.get_user(username)
            return user
