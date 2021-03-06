from __future__ import annotations

import hashlib
from contextlib import AbstractAsyncContextManager
from random import random
from types import TracebackType
from typing import Optional, Type

from ._rest import GitHubSession, Repository, User

SESSION_ATTR_NAME: str = hashlib.sha256(
    str(random()).encode("utf-8")
).hexdigest()


class GitHub(AbstractAsyncContextManager):

    username: str
    token: str
    is_token_auth: bool
    session: GitHubSession
    _user: Optional[User]

    def __init__(
        self, username: str, token: str, is_token_auth: bool = False
    ) -> None:
        """Async GitHub client.

        All async calls to methods of this object and objects
        created with calls to methods of instance of this object
        should be done within async with code block.

        Objects created by this objects are bound to this object
        and are able to communicate with Github API only by this
        object session (async with block) unless manually rebound to
        different object.

        Parameters
        ----------
        username : str
            Github account user name.
        token : str
            Access token for same account as username was.
        is_token_auth : bool, optional
            When True, token only authentication is used, basic auth otherwise, by default False
        """
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
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        return await self.session.__aexit__(exc_type, exc_val, exc_tb)

    def get_gh_session(self) -> GitHubSession:
        return self.session

    async def user(self, username: Optional[str] = None) -> User:
        """Request github user details from Github API. This function requires
        internet connection, thus have to be called within `async` `with`
        block.

        Parameters
        ----------
        username : Optional[str], optional
            Login of user to acquire, when none, details for currently
            authenticated user are returned.

        Returns
        -------
        User
            Wrapper object containing user details and allowing for
            further API interaction.
        """
        if username is None:
            if self._user is None:  # pragma: no cover
                self._user = await self.session.get_user()
            assert self._user is not None
            return self._user
        else:
            user = await self.session.get_user(username)
            return user

    async def repository(self, user_name: str, repo_name: str) -> Repository:
        """Request github repository owned by `user_name` with name
        `repo_name`. It is alternative to first requesting user and then
        requesting repo using User object API.

        Parameters
        ----------
        user_name : str
            Name of owner of repo.
        repo_name : str
            Name of repository requested.

        Returns
        -------
        Repository
            Wrapper object containing details of repo and allowing for further
            API interaction.
        """
        return await self.session.get_repo(user_name, repo_name)
