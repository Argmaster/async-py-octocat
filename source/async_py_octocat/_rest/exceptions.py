from __future__ import annotations

__all__ = [
    "RequiresAuthentication401",
    "MovedPermanently301",
    "NotModified304",
    "Forbidden403",
    "NotFound404",
    "SessionNotAvailable",
    "SessionNotClosed",
]


class ResponseError(Exception):
    pass


class MovedPermanently301(ResponseError):
    pass


class NotModified304(ResponseError):
    pass


class RequiresAuthentication401(ResponseError):
    pass


class Forbidden403(ResponseError):
    pass


class NotFound404(ResponseError):
    pass


class SessionError(Exception):
    pass


class SessionNotAvailable(SessionError):
    pass


class SessionNotClosed(SessionError):
    pass
