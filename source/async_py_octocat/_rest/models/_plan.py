from __future__ import annotations

from ._response import RestResponse

__all__ = ["Plan"]


class Plan(RestResponse):
    """Plan (Sometimes available with user profile data) wrapper &
    validator."""

    name: str
    space: int
    collaborators: int
    private_repos: int
