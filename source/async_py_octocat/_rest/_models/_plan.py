from __future__ import annotations

from ._response import RestResponse

__all__ = ["Plan"]


class Plan(RestResponse):
    name: str
    space: int
    collaborators: int
    private_repos: int
