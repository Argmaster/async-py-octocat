import json
from pathlib import Path

from async_py_octocat import Repository

DIR = Path(__file__).parent
DATA_DIR = DIR / "data"

EXAMPLE_PY_OCTO = json.loads(
    (DATA_DIR / "repo_py_octo.json").read_text("utf-8")
)
EXAMPLE_DOC = json.loads((DATA_DIR / "repo_example.json").read_text("utf-8"))


class TestRepository:
    def test_parse_example(self) -> None:
        repo = Repository(**EXAMPLE_DOC)

        assert repo.owner.email is None
        assert repo.owner.followers is None
        assert repo.owner.created_at is None

    def test_second_example(self) -> None:
        repo = Repository(**EXAMPLE_PY_OCTO)

        assert repo.owner.email is None
        assert repo.owner.followers is None
        assert repo.owner.created_at is None
