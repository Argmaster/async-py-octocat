import argparse
import re
import sys
from pathlib import Path
from typing import List

SCRIPTS_DIR = Path(__file__).parent
REPOSITORY_ROOT_DIR = SCRIPTS_DIR.parent
SOURCE_DIR = REPOSITORY_ROOT_DIR / "source" / "async_py_octocat"


VERSION_REGEX = re.compile(r'''__version__.*?=.*?"(\d+\.\d+\.\d+.*?)"''')


def fetch_version(init_file: Path) -> str:
    """Fetch package version from root `__init__.py` file."""
    with init_file.open("r", encoding="utf-8") as file:
        version_math = VERSION_REGEX.search(file.read())
        assert version_math is not None
        return version_math.group(1)


def main(argv: List[str]):
    parser = argparse.ArgumentParser("get_version.py")
    parser.add_argument("--prefix", "-p", required=False, default="")
    parser.add_argument("--suffix", "-s", required=False, default="")
    args = parser.parse_args(argv)

    version = fetch_version(SOURCE_DIR / "__init__.py")

    print(f"{args.prefix}{version}{args.suffix}")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
