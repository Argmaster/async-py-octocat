import pytest

from async_py_octocat import GitHub, User


class TestGitHub:
    @pytest.mark.asyncio()
    async def test_with_basic_auth(
        self, gh_username: str, gh_token_full: str
    ) -> None:
        client = await GitHub(gh_username, gh_token_full)
        assert isinstance(client.user, User)
