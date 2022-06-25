from pathlib import Path
from typing import List

import pytest

from .cli_toggle import Behavior, register_toggle

register_toggle(
    cli_flag="benchmark",
    cli_flag_doc="Run only tests marked as benchmarks.",
    pytest_mark_name="benchmark",
    pytest_mark_doc="Benchmark tests were not enabled explicitly.",
    flag_behavior=Behavior.INCLUDE_WHEN_FLAG_AND_EXCLUDE_OTHERS,
)


def pytest_addoption(parser: pytest.Parser):  # pragma: no cover
    register_toggle.pytest_addoption(parser)


def pytest_configure(config: pytest.Config):  # pragma: no cover
    register_toggle.pytest_configure(config)


def pytest_collection_modifyitems(
    session: pytest.Session,
    config: pytest.Config,
    items: List[pytest.Item],
):  # pragma: no cover
    register_toggle.pytest_collection_modifyitems(session, config, items)


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
