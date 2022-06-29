import pytest

from async_py_octocat._rest import GitHubSession


class TestGitHubSession:
    @pytest.mark.parametrize("is_token_auth", [True, False])
    @pytest.mark.asyncio()
    async def test_gh_session(
        self,
        gh_username: str,
        gh_token_full: str,
        is_token_auth: bool,
    ) -> None:
        gh_session = GitHubSession(gh_username, gh_token_full, is_token_auth)

        async with gh_session as session:
            assert isinstance(session, GitHubSession)
