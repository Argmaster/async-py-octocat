from __future__ import annotations

from typing import TYPE_CHECKING

from typing_extensions import Protocol

if TYPE_CHECKING:
    from ._rest.session import GitHubSession


__all__ = ["HasGHSessionProtocol"]


class HasGHSessionProtocol(Protocol):
    def get_gh_session(self) -> GitHubSession:
        ...
