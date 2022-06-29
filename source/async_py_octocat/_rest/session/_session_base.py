from __future__ import annotations

import hashlib
from random import random
from types import TracebackType
from typing import Any, Dict, Type, TypeVar

import aiohttp
from aiohttp import ClientSession

from ..exceptions import SessionNotAvailable, SessionNotClosed

__all__ = ["SessionBase"]


SESSION_ATTR_NAME: str = hashlib.sha256(
    str(random()).encode("utf-8")
).hexdigest()

T = TypeVar("T", bound="SessionBase")


class SessionBase:

    username: str
    token: str
    is_token_auth: bool
    extra: Dict[str, Any]

    def __init__(
        self, username: str, token: str, is_token_auth: bool, **extra: Any
    ) -> None:
        self.username = username
        self.token = token
        self.is_token_auth = is_token_auth
        self.extra = extra

    async def set_client_session(self) -> None:
        if not hasattr(self, SESSION_ATTR_NAME):
            return setattr(
                self,
                SESSION_ATTR_NAME,
                ClientSession(**self._get_session_kwargs()),
            )
        raise SessionNotClosed(
            "Session was not correctly closed before creating new session."
        )

    def _get_session_kwargs(
        self,
    ) -> Dict[str, Any]:
        if self.is_token_auth:
            kwargs = {
                "headers": {
                    "Accept": "application/vnd.github.v3+json",
                    "Authorization": f"token {self.token}",
                },
            }
        else:
            kwargs = {
                "auth": aiohttp.BasicAuth(
                    login=self.username, password=self.token
                ),
                "headers": {"Accept": "application/vnd.github.v3+json"},
            }

        kwargs.update(self.extra)
        return kwargs

    @property
    def client_session(self) -> ClientSession:
        return self.get_client_session()

    def get_client_session(self) -> ClientSession:
        session = getattr(self, SESSION_ATTR_NAME, None)
        if session is None:
            raise SessionNotAvailable("Session was not properly initialized.")
        return session

    async def del_client_session(self) -> None:
        session = self.get_client_session()
        if not session.closed:
            await session.close()
        delattr(self, SESSION_ATTR_NAME)
        assert SESSION_ATTR_NAME not in self.__dict__.keys()

    async def __aenter__(self: T) -> T:
        await self.set_client_session()
        await self.get_client_session().__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType,
    ) -> None:
        retval = await self.get_client_session().__aexit__(
            exc_type, exc_val, exc_tb
        )
        await self.del_client_session()
        return retval
