from __future__ import annotations

from pydantic import HttpUrl

from ._response import RestResponse

__all__ = ["Organization"]


class Organization(RestResponse):
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
