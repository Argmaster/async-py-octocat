from async_py_octocat.common.url import GHUrl, is_url, parse_repo_from


def test_is_url():
    assert is_url("https://github.com/Argmaster/async-py-octocat.git")
    assert is_url("http://github.com/Argmaster/async-py-octocat")
    assert is_url("https://github.com/python-pillow/Pillow")


def test_parse_name_from_url():
    assert parse_repo_from(
        "https://github.com/Argmaster/async-py-octocat.git"
    ) == GHUrl(owner="Argmaster", repo="async-py-octocat")

    assert parse_repo_from("http://github.com/python-pillow/Pillow") == GHUrl(
        owner="python-pillow", repo="Pillow"
    )
