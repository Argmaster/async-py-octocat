import re

from pydantic import BaseModel

_URL_PATTERN = re.compile(r"https?://.*")
_URL_PARSE_PATTERN = re.compile(
    r"^https?://.*?github.*?/(?P<owner>.+?)/(?P<repo>.*?)(?:\.git)?(?:/.*)?$"
)


__all__ = ["is_url", "parse_repo_from", "GHUrl"]


def is_url(string: str) -> bool:
    return _URL_PATTERN.match(string) is not None


class GHUrl(BaseModel):

    owner: str
    repo: str


def parse_repo_from(url: str) -> GHUrl:
    re_match = _URL_PARSE_PATTERN.search(url)
    assert re_match is not None
    return GHUrl(**re_match.groupdict())
