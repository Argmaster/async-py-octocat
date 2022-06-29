from __future__ import annotations

from typing import Optional

from pydantic import Field

from ...types import HasGHSessionProtocol
from ..exceptions import SessionNotAvailable
from ..session import GitHubSession
from ._response import RestResponse

__all__ = ["Interactive"]


class Interactive(RestResponse):

    gh_session_object: Optional[GitHubSession] = Field(default=None)

    class Config(RestResponse.Config):
        keep_untouched = (*RestResponse.Config.keep_untouched, GitHubSession)

    def get_gh_session(self) -> GitHubSession:
        if self.gh_session_object is None:
            raise SessionNotAvailable(
                "Session is not available, probably this object was "
                "created manually without session bound. "
                "You can manually set session using bind_session()"
            )
        return self.gh_session_object

    def bind_gh_session(self, has_session: HasGHSessionProtocol) -> None:
        self.__dict__["gh_session_object"] = has_session.get_gh_session()
