from unittest.mock import MagicMock, patch

import pytest

from async_py_octocat._rest import GitHubSession


class TestGitHubSession:
    @pytest.mark.parametrize("is_token_auth", [True, False])
    @pytest.mark.asyncio()
    @patch("async_py_octocat._rest.session._session_base.SessionBase")
    async def test_gh_session_mocked(
        self, mock_class, is_token_auth: bool
    ) -> None:
        from async_py_octocat._rest.session._session_base import SessionBase

        assert SessionBase is mock_class

        gh_session = GitHubSession("username", "token", is_token_auth)

        async with gh_session as session:
            assert isinstance(session, GitHubSession)

    @pytest.mark.parametrize("is_token_auth", [True, False])
    @pytest.mark.asyncio()
    async def test_gh_session(
        self,
        gh_username: str,
        gh_token_full: str,
        is_token_auth: bool,
    ) -> None:
        from async_py_octocat._rest.session._session_base import SessionBase

        assert not isinstance(SessionBase, MagicMock)

        gh_session = GitHubSession(gh_username, gh_token_full, is_token_auth)

        async with gh_session as session:
            assert isinstance(session, GitHubSession)
