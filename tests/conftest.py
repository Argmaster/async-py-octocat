from pathlib import Path
from typing import List, Optional

import pytest

GH_USERNAME: Optional[str] = None
GH_TOKEN_FULL: Optional[str] = None
GH_TOKEN_LIMITED: Optional[str] = None


def pytest_addoption(parser: pytest.Parser):  # pragma: no cover
    parser.addoption("--gh-username", default=None)
    parser.addoption("--gh-token-full", default=None)
    parser.addoption("--gh-token-limited", default=None)


def pytest_configure(config: pytest.Config):  # pragma: no cover
    global GH_USERNAME
    temp = config.getoption("--gh-username")
    assert isinstance(temp, str), temp
    GH_USERNAME = temp

    global GH_TOKEN_FULL
    temp = config.getoption("--gh-token-full")
    assert isinstance(temp, str)
    GH_TOKEN_FULL = temp

    global GH_TOKEN_LIMITED
    temp = config.getoption("--gh-token-limited")
    assert isinstance(temp, str)
    GH_TOKEN_LIMITED = temp


def pytest_collection_modifyitems(
    session: pytest.Session,
    config: pytest.Config,
    items: List[pytest.Item],
):  # pragma: no cover
    ...


@pytest.fixture(scope="session")
def test_dir() -> Path:  # pragma: no cover
    return Path(__file__).parent


@pytest.fixture(scope="session")
def repo_dir() -> Path:  # pragma: no cover
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def source_dir(repo_dir: Path) -> Path:  # pragma: no cover
    return repo_dir / "source"


@pytest.fixture(scope="session")
def package_dir(source_dir: Path) -> Path:  # pragma: no cover
    return source_dir / "async_py_octocat"


@pytest.fixture(scope="session")
def gh_username() -> str:
    assert isinstance(GH_USERNAME, str)
    return GH_USERNAME


@pytest.fixture(scope="session")
def gh_token_full() -> str:
    assert isinstance(GH_TOKEN_FULL, str)
    return GH_TOKEN_FULL


@pytest.fixture(scope="session")
def gh_token_limited() -> str:
    assert isinstance(GH_TOKEN_LIMITED, str)
    return GH_TOKEN_LIMITED
