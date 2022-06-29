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
