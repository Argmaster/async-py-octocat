import json
from pathlib import Path

import pytest

from async_py_octocat._rest._models._user import User

DIR = Path(__file__).parent
DATA_DIR = DIR / "data"

EXAMPLE_PUBLIC = json.loads((DATA_DIR / "user_pub.json").read_text("utf-8"))
EXAMPLE_PRIVATE = json.loads((DATA_DIR / "user_priv.json").read_text("utf-8"))


class TestUser:
    def test_parse_example_public_json(self):
        User(**EXAMPLE_PUBLIC)

    def test_parse_example_private_json(self):
        User(**EXAMPLE_PRIVATE)

    @pytest.mark.asyncio()
    async def test_fail_repo(self):
        with pytest.raises(AttributeError):
            await User(**EXAMPLE_PRIVATE).repo("fails anyway")
