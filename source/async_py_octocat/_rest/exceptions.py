from __future__ import annotations

__all__ = [
    "RequiresAuthentication401",
    "MovedPermanently301",
    "NotModified304",
    "Forbidden403",
    "NotFound404",
]


class MovedPermanently301(ConnectionError):
    pass


class NotModified304(ConnectionError):
    pass


class RequiresAuthentication401(ConnectionError):
    pass


class Forbidden403(ConnectionError):
    pass


class NotFound404(ConnectionError):
    pass
