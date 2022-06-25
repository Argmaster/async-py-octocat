from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import Field, HttpUrl

from ._plan import Plan
from ._response import RestResponse


class User(RestResponse):

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
    name: Optional[str]
    company: Optional[str]
    blog: str
    location: Optional[str]
    email: Optional[str]
    hireable: Optional[str]
    bio: Optional[str]
    twitter_username: Optional[str]
    public_repos: int
    public_gists: int
    followers: int
    following: int
    created_at: datetime
    updated_at: datetime
    private_gists: Optional[int] = Field(default=None)
    total_private_repos: Optional[int] = Field(default=None)
    owned_private_repos: Optional[int] = Field(default=None)
    disk_usage: Optional[int] = Field(default=None)
    collaborators: Optional[int] = Field(default=None)
    two_factor_authentication: Optional[bool] = Field(default=None)
    plan: Optional[Plan] = Field(default=None)
