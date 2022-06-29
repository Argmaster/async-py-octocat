import pytest

from async_py_octocat import (
    GitHub,
    Plan,
    Repository,
    SessionNotAvailable,
    User,
)

ALT_USER: str = "Argmaster"
REPO_NAME: str


class TestGitHub:
    def check_user_private_fields_populated(self, user: User) -> None:
        assert isinstance(user.private_gists, int)
        assert isinstance(user.total_private_repos, int)
        assert isinstance(user.owned_private_repos, int)
        assert isinstance(user.disk_usage, int)
        assert isinstance(user.collaborators, int)
        assert isinstance(user.two_factor_authentication, bool)
        assert isinstance(user.plan, Plan)

    def check_user_private_fields_empty(self, user: User) -> None:
        assert user.private_gists is None
        assert user.total_private_repos is None
        assert user.owned_private_repos is None
        assert user.disk_usage is None
        assert user.collaborators is None
        assert user.two_factor_authentication is None
        assert user.plan is None

    @pytest.mark.parametrize("use_token_auth", [True, False])
    @pytest.mark.asyncio()
    async def test_with_token_full_basic_auth(
        self, gh_username: str, gh_token_full: str, use_token_auth: bool
    ) -> None:
        async with GitHub(
            gh_username, gh_token_full, use_token_auth
        ) as client:
            user = await client.user()

        assert isinstance(user, User)
        self.check_user_private_fields_populated(user)

    @pytest.mark.parametrize("use_token_auth", [True, False])
    @pytest.mark.asyncio()
    async def test_with_token_limited_basic_auth(
        self, gh_username: str, gh_token_limited: str, use_token_auth: bool
    ) -> None:
        async with GitHub(
            gh_username, gh_token_limited, use_token_auth
        ) as client:
            user = await client.user()

        assert isinstance(user, User)
        self.check_user_private_fields_empty(user)

    @pytest.mark.asyncio()
    async def test_get_auth_user_no_credential_validation(
        self, gh_username: str, gh_token_full: str
    ):
        async with GitHub(gh_username, gh_token_full) as client:
            user = await client.user()

        assert isinstance(user, User)
        self.check_user_private_fields_populated(user)

    @pytest.mark.asyncio()
    async def test_get_arbitrary_user(
        self, gh_username: str, gh_token_full: str
    ):
        async with GitHub(gh_username, gh_token_full) as client:
            user = await client.user(ALT_USER)

        assert isinstance(user, User)
        self.check_user_private_fields_empty(user)

    @pytest.mark.asyncio()
    async def test_get_user_repo(self, gh_username: str, gh_token_full: str):
        async with GitHub(gh_username, gh_token_full) as client:
            user = await client.user(ALT_USER)
            repo = await user.repo("async-py-octocat")

        assert isinstance(repo, Repository), repo

    @pytest.mark.asyncio()
    async def test_fail_get_user_session_ended(
        self, gh_username: str, gh_token_full: str
    ):
        async with GitHub(gh_username, gh_token_full) as client:
            pass
        with pytest.raises(SessionNotAvailable):
            await client.user(ALT_USER)
