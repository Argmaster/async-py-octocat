from __future__ import annotations

from unittest.mock import MagicMock, Mock

from async_py_octocat import GitHub
from async_py_octocat._rest.models._interactive import Interactive
from async_py_octocat._rest.session import GitHubSession


class TestInteractive:
    def test_rebind_from_interactive(self) -> None:
        gh_session_mock = Mock(spec=GitHubSession)
        other = Interactive(gh_session_object=gh_session_mock)

        interactive = Interactive()
        interactive.bind_gh_session(other)

        assert interactive.get_gh_session() == gh_session_mock

    def test_rebind_from_github(self) -> None:
        gh = object.__new__(GitHub)
        assert isinstance(gh, GitHub)
        gh_session_mock = MagicMock()
        gh.session = gh_session_mock

        interactive = Interactive()
        interactive.bind_gh_session(gh)

        assert interactive.get_gh_session() == gh_session_mock

    def test_rebind_from_github_session(self) -> None:
        gh = object.__new__(GitHubSession)
        assert isinstance(gh, GitHubSession)

        interactive = Interactive()
        interactive.bind_gh_session(gh)

        assert interactive.get_gh_session() == gh
