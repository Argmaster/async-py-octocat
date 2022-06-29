import hashlib
import json
from contextlib import asynccontextmanager
from pathlib import Path
from random import random
from typing import AsyncGenerator

import pytest

from async_py_octocat import (
    NotFound404,
    Repository,
    RequiresAuthentication401,
    SessionNotAvailable,
    User,
)
from async_py_octocat._rest.session import GitHubSession

DIR = Path(__file__).parent
DATA_DIR = DIR / "data"

EXAMPLE_PUBLIC = json.loads((DATA_DIR / "user_pub.json").read_text("utf-8"))
EXAMPLE_PRIVATE = json.loads((DATA_DIR / "user_priv.json").read_text("utf-8"))

ALT_USER: str = "Argmaster"
REPO_NAME: str = "async-py-octocat"
REPO_URL: str = "https://github.com/Argmaster/async-py-octocat"

RANDOM_SHA256: str = hashlib.sha256(str(random()).encode("utf-8")).hexdigest()


@asynccontextmanager
async def get_user(
    gh_username: str,
    gh_token_full: str,
    is_token_auth: bool,
) -> AsyncGenerator[User, None]:
    async with GitHubSession(
        gh_username, gh_token_full, is_token_auth
    ) as gh_session:
        user = await gh_session.get_user(ALT_USER)
        yield user


class TestUser:
    def test_parse_example_public_json(self) -> None:
        User(**EXAMPLE_PUBLIC)

    def test_parse_example_private_json(self) -> None:
        User(**EXAMPLE_PRIVATE)

    @pytest.mark.asyncio()
    async def test_fail_repo(self) -> None:
        with pytest.raises(SessionNotAvailable):
            await User(**EXAMPLE_PRIVATE).repo("fails anyway")

    @pytest.mark.parametrize("is_token_auth", [True, False])
    @pytest.mark.asyncio()
    async def test_acquire_repository(
        self,
        gh_username: str,
        gh_token_full: str,
        is_token_auth: bool,
    ) -> None:
        async with get_user(gh_username, gh_token_full, is_token_auth) as user:
            repo = await user.repo(REPO_NAME)
            assert isinstance(repo, Repository)
            assert repo.name == REPO_NAME
            assert repo.owner.login == ALT_USER
            assert repo.fork is False
            assert repo.is_template is False

    @pytest.mark.parametrize(
        ("is_token_auth", "source"),
        [
            (True, REPO_NAME),
            (True, REPO_URL),
            (False, REPO_NAME),
            (False, REPO_URL),
        ],
    )
    @pytest.mark.asyncio()
    async def test_alternative_acquire_repository(
        self,
        gh_username: str,
        gh_token_full: str,
        is_token_auth: bool,
        source: str,
    ) -> None:
        async with get_user(gh_username, gh_token_full, is_token_auth) as user:
            repo1 = await user.repo(source)
            repo2 = await user.repository(source)
            assert repo1 == repo2

    @pytest.mark.asyncio()
    async def test_fail_no_auth_with_token(self) -> None:
        async with GitHubSession("anyone", "token", True) as gh_session:
            with pytest.raises(RequiresAuthentication401):
                await gh_session.get_user()

            with pytest.raises(RequiresAuthentication401):
                await gh_session.get_user(RANDOM_SHA256)

    @pytest.mark.asyncio()
    async def test_fail_no_auth_with_base_auth(self) -> None:
        async with GitHubSession("anyone", "token", False) as gh_session:
            with pytest.raises(RequiresAuthentication401):
                await gh_session.get_user()

            with pytest.raises(NotFound404):
                await gh_session.get_user(RANDOM_SHA256)

    @pytest.mark.parametrize("is_token_auth", [True, False])
    @pytest.mark.asyncio()
    async def test_bind_gh_session_short(
        self,
        gh_username: str,
        gh_token_full: str,
        is_token_auth: bool,
    ) -> None:
        # get user from session #1
        async with GitHubSession(
            gh_username, gh_token_full, is_token_auth
        ) as gh_session:
            user = await gh_session.get_user(ALT_USER)
        # enter session #2 and rebind user to it
        async with GitHubSession(
            gh_username, gh_token_full, is_token_auth
        ) as gh_session2:
            assert gh_session == user.get_gh_session()
            user.bind_gh_session(gh_session2)
            # ensure rebind was done correctly
            assert gh_session2 == user.get_gh_session()
            # check wether user can correctly use new session (#2)
            repo = await user.repository(REPO_NAME)
            assert repo.name == REPO_NAME
            assert repo.owner.login == ALT_USER

    @pytest.mark.parametrize("is_token_auth", [True, False])
    @pytest.mark.asyncio()
    async def test_bind_gh_session_extended(
        self,
        gh_username: str,
        gh_token_full: str,
        is_token_auth: bool,
    ) -> None:
        # get user from session #1
        async with GitHubSession(
            gh_username, gh_token_full, is_token_auth
        ) as gh_session:
            user = await gh_session.get_user(ALT_USER)
        # create new session (#2) object to rebind user to
        gh_session2 = GitHubSession(gh_username, gh_token_full, is_token_auth)
        # enter session #2 and rebind user to it
        async with gh_session2:
            user.bind_gh_session(gh_session2)
        # check wether user no longer can use session outside async with
        with pytest.raises(SessionNotAvailable):
            await user.repository(REPO_NAME)
        # reset session (#2) and check wether user can correctly use it again
        async with gh_session2:
            repo = await user.repo(REPO_NAME)
            assert repo.name == REPO_NAME
            assert repo.owner.login == ALT_USER
        # check wether user no longer can use session after session reset
        with pytest.raises(SessionNotAvailable):
            await user.repository(REPO_NAME)
