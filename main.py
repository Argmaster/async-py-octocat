from __future__ import annotations

import asyncio


class Ctx:
    def __init__(self, name) -> None:
        self.name = name

    async def __aenter__(self) -> Ctx:
        print(f"AEnter {self.name}")
        return self

    async def __aexit__(self, *_):
        print(f"AExit {self.name}")

    async def function(self, name):
        print(f"Function {name} begin")
        await asyncio.sleep(1)
        print(f"Function {name} end")


async def main():
    async with Ctx("1") as ctx1:
        async with Ctx("2") as ctx2:
            await asyncio.gather(
                ctx1.function("1.1"),
                ctx2.function("2.2"),
                ctx2.function("2.3"),
            )

        await ctx1.function("1.2")


asyncio.run(main())
