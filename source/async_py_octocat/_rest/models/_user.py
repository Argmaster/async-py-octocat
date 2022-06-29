from __future__ import annotations

from datetime import datetime
from typing import Optional, Union

from pydantic import Field, HttpUrl

from async_py_octocat.common import is_url, parse_repo_from

from . import _repository
from ._interactive import Interactive
from ._plan import Plan

__all__ = ["User"]


class User(Interactive):

    """User profile data wrapper & validator.

    Thanks to BaseModel inheritance, JSON data acquired from github api
    endpoint can be automatically dispatched and validated.
    """

    # public profile information:
    login: str
    id: int  # noqa: A003
    node_id: str
    avatar_url: str
    gravatar_id: str
    url: HttpUrl
    html_url: HttpUrl
    followers_url: HttpUrl
    following_url: HttpUrl
    gists_url: HttpUrl
    starred_url: HttpUrl
    subscriptions_url: HttpUrl
    organizations_url: HttpUrl
    repos_url: HttpUrl
    events_url: HttpUrl
    received_events_url: HttpUrl
    type: str  # noqa: A003
    site_admin: bool
    # fields not available in repository description
    name: str = Field(default=None)
    company: str = Field(default=None)
    blog: str = Field(default=None)
    location: str = Field(default=None)
    email: str = Field(default=None)
    hireable: str = Field(default=None)
    bio: str = Field(default=None)
    twitter_username: str = Field(default=None)
    public_repos: int = Field(default=None)
    public_gists: int = Field(default=None)
    followers: int = Field(default=None)
    following: int = Field(default=None)
    created_at: datetime = Field(default=None)
    updated_at: datetime = Field(default=None)
    # private profile information:
    private_gists: Optional[int]
    total_private_repos: Optional[int]
    owned_private_repos: Optional[int]
    disk_usage: Optional[int]
    collaborators: Optional[int]
    two_factor_authentication: Optional[bool]
    plan: Optional[Plan]

    async def repo(
        self, name_or_url: Union[str, HttpUrl]
    ) -> _repository.Repository:
        return await self._fetch_repository(name_or_url)

    async def repository(
        self, name_or_url: Union[str, HttpUrl]
    ) -> _repository.Repository:
        return await self._fetch_repository(name_or_url)

    async def _fetch_repository(
        self, name_or_url: Union[str, HttpUrl]
    ) -> _repository.Repository:
        # decide whether url string or just name was given
        str_guarantee = str(name_or_url)
        if is_url(str_guarantee):
            repo_name = parse_repo_from(str_guarantee).repo
        else:
            repo_name = str_guarantee
        repo = await self.get_session().get_repo(self.login, repo_name)

        return repo
