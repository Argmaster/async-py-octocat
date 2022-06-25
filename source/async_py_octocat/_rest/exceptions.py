from __future__ import annotations

__all__ = ["RequiresAuthentication401", "NotModified304", "Forbidden403"]


class RequiresAuthentication401(ConnectionError):
    pass


class NotModified304(ConnectionError):
    pass


class Forbidden403(ConnectionError):
    pass
