![Async PyOctocat](https://raw.githubusercontent.com/Argmaster/async-py-octocat/main/docs/img/bg.jpg)

Async PyOctocat is a Python library for asynchronous interaction with GitHub
API. I was pushed to create this library by the lack of an actively maintained
and well documented asynchronous library that would allow quick and efficient
high-level interaction with Github from code. I sincerely hope that one day
this library can be said to be actively maintained and well documented.

## Install

```
pip install async_py_octocat
```

## Features

Due to the extensiveness of the Github API, functionalities require incremental
implementation, and at this point PyOctocat is far from having all endpoints
finished. Check Features Status section in our documentation to learn about
features which are already available.

## Example

```python
import asyncio

from async_py_octocat import GitHub

gh_username: str = "Your Username"
gh_token_full: str = "ghp_..."  # your token


async def main():
    async with GitHub(gh_username, gh_token_full) as client:
        # by default .user() method returns currently authenticated user
        currently_authenticated = await client.user()
        print(currently_authenticated)

        # to get other user just pass username as first argument
        other_user = await client.user("Other User name")
        print(other_user)

        # to download repository owned by some user you can use
        # previously acquired User object
        repo = await currently_authenticated.repository("repo_name")
        print(repo)


if __name__ == "__main__":
    asyncio.run(main())

```

For full tutorial check out Quick Start section in our docs.

## Documentation

Online documentation is available at
[argmaster.github.io/async_py_octocat/](https://argmaster.github.io/async_py_octocat/)

To build docs locally run

```
tox -e docs
```
