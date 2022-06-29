from __future__ import annotations

import pytest
from aiohttp import ClientSession

from async_py_octocat import SessionNotClosed
from async_py_octocat._rest.exceptions import SessionNotAvailable
from async_py_octocat._rest.session._session_base import (
    SESSION_ATTR_NAME,
    SessionBase,
)


class TestSessionBase:
    @pytest.mark.parametrize("is_token_auth", [True, False])
    @pytest.mark.asyncio()
    async def test_set_client_session(
        self,
        gh_username: str,
        gh_token_full: str,
        is_token_auth: bool,
    ) -> None:
        gh_session = SessionBase(gh_username, gh_token_full, is_token_auth)
        await gh_session.set_client_session()

        assert SESSION_ATTR_NAME in gh_session.__dict__
        session_object = gh_session.__dict__[SESSION_ATTR_NAME]
        assert isinstance(session_object, ClientSession)
        assert session_object.closed is False

    @pytest.mark.parametrize("is_token_auth", [True, False])
    @pytest.mark.asyncio()
    async def test_double_set_fails(
        self,
        gh_username: str,
        gh_token_full: str,
        is_token_auth: bool,
    ) -> None:
        gh_session = SessionBase(gh_username, gh_token_full, is_token_auth)
        await gh_session.set_client_session()

        with pytest.raises(SessionNotClosed):
            await gh_session.set_client_session()

    @pytest.mark.parametrize("is_token_auth", [True, False])
    @pytest.mark.asyncio()
    async def test_set_get_session(
        self,
        gh_username: str,
        gh_token_full: str,
        is_token_auth: bool,
    ) -> None:
        gh_session = SessionBase(gh_username, gh_token_full, is_token_auth)
        await gh_session.set_client_session()
        session = gh_session.get_client_session()

        assert isinstance(session, ClientSession)

    @pytest.mark.parametrize("is_token_auth", [True, False])
    @pytest.mark.asyncio()
    async def test_get_session_not_set_fails(
        self,
        gh_username: str,
        gh_token_full: str,
        is_token_auth: bool,
    ) -> None:
        gh_session = SessionBase(gh_username, gh_token_full, is_token_auth)

        with pytest.raises(SessionNotAvailable):
            gh_session.get_client_session()

    @pytest.mark.parametrize("is_token_auth", [True, False])
    @pytest.mark.asyncio()
    async def test_del_not_set_session(
        self,
        gh_username: str,
        gh_token_full: str,
        is_token_auth: bool,
    ) -> None:
        gh_session = SessionBase(gh_username, gh_token_full, is_token_auth)
        with pytest.raises(SessionNotAvailable):
            await gh_session.del_client_session()

    @pytest.mark.parametrize("is_token_auth", [True, False])
    @pytest.mark.asyncio()
    async def test_set_get_del_session(
        self,
        gh_username: str,
        gh_token_full: str,
        is_token_auth: bool,
    ) -> None:
        gh_session = SessionBase(gh_username, gh_token_full, is_token_auth)
        await gh_session.set_client_session()
        session = gh_session.get_client_session()

        assert isinstance(session, ClientSession)
        await gh_session.del_client_session()

        with pytest.raises(SessionNotAvailable):
            gh_session.get_client_session()

    @pytest.mark.parametrize("is_token_auth", [True, False])
    @pytest.mark.asyncio()
    async def test_context_manager(
        self,
        gh_username: str,
        gh_token_full: str,
        is_token_auth: bool,
    ) -> None:
        gh_session = SessionBase(gh_username, gh_token_full, is_token_auth)
        async with gh_session as session:
            assert isinstance(session, SessionBase)
            assert isinstance(gh_session.get_client_session(), ClientSession)
