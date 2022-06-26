from __future__ import annotations

from ._response import RestResponse

__all__ = ["Permissions"]


class Permissions(RestResponse):
    pull: bool
    push: bool
    admin: bool
