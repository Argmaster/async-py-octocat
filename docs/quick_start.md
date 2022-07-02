# Quick Start

Welcome to quick start section. We will explain here how to get started using
the PyOctocat library.

## Creating a GitHub client

As library name implies, PyOctocat is mainly designed to be asynchronous
library and thus requires code to be run in `#!python async` functions.
Therefore basic template which will be used for rest of this tutorial looks
following way:

```python
import asyncio


async def main():
    ...


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))

```

All executable code goes into `#!python async def main()` function shown above.
Imports can be still kept at the top of the file (and it is recommended).

To begin with using PyOctocat, you will have to create instance of GitHub
object, which takes username and github token as arguments. It will be used to
acquire objects from Github API and control session availability.

```python
import asyncio
from async_py_octocat import GitHub


async def main():
    gh = GitHub("username", "ghp_...")
    ...


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))

```

## Interacting with Github API

Now when you have created Github client object, active interaction (sending and
receiving data) can only be done withing `#!python async with` block in
`#!python async` function. All interaction, requiring internet access, outside
`#!python async with`, will fail.

```python
import asyncio
from async_py_octocat import GitHub


async def main():
    gh = GitHub("username", "ghp_...")
    async with gh as client:
        ...


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
```

At this point we can acquire user information via Github API with call to
`.user(...)` function. When called with no arguments, it will return currently
authenticated user, otherwise expects string containing user name and returns
wrapper object containing details acquired from API.

```python
import asyncio
from async_py_octocat import GitHub


async def main():
    gh = GitHub("username", "ghp_...")
    async with gh as client:
        user = client.user("Argmaster")
        ...

if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
```

Having the user object, we can get the repository of which he is the owner. We
do this by using the repository() method, which takes the name of the
repository as an argument.

```python
import asyncio
from async_py_octocat import GitHub


async def main():
    gh = GitHub("username", "ghp_...")
    async with gh as client:
        user = await client.user("Argmaster")
        repo = await user.repository("repo_name")
        ...

if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
```

!!! info

    Your next steps depend on your needs, unfortunately rest of API is currently
    not implemented. Hopefully, in the next release we will put in your hands the
    tools to use the data contained in the repository.
