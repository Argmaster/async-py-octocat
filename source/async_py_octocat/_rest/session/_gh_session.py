from __future__ import annotations

import json
from typing import Optional

from .._constants import BASE_URL
from ..exceptions import (
    Forbidden403,
    MovedPermanently301,
    NotFound404,
    NotModified304,
    RequiresAuthentication401,
)
from ..models import _repository as repository
from ..models import _user as user
from ._session_base import SessionBase

__all__ = ["GitHubSession"]


GET_AUTH_USER: str = f"{BASE_URL}/user"
GET_ANY_USER: str = f"{BASE_URL}/users"
GET_REPO: str = f"{BASE_URL}/repos"


class GitHubSession(SessionBase):
    async def get_user(self, username: Optional[str] = None) -> user.User:
        if username is None:
            return await self._get_user(GET_AUTH_USER)
        else:
            return await self._get_user(f"{GET_ANY_USER}/{username}")

    async def _get_user(self, url: str) -> user.User:
        async with self.client_session.get(url) as response:
            content = await response.text()
            if response.status == 401:
                raise RequiresAuthentication401(content)
            if response.status == 304:
                raise NotModified304(content)
            if response.status == 403:
                raise Forbidden403(content)
            assert response.status == 200, response
        content_object = json.loads(content)
        return user.User(**content_object, gh_session_object=self)

    async def get_repo(self, owner: str, repo: str) -> repository.Repository:
        async with self.client_session.get(
            f"{GET_REPO}/{owner}/{repo}"
        ) as response:
            content = await response.text()
            if response.status == 301:
                raise MovedPermanently301(content)
            if response.status == 403:
                raise Forbidden403(content)
            if response.status == 404:
                raise NotFound404(content)
            assert response.status == 200, response
        content_object = json.loads(content)
        return repository.Repository(**content_object, gh_session_object=self)
