import asyncio
from time import time
from typing import List, Tuple, Optional

import aiohttp
import requests
from aiohttp import ClientSession


def test_request(n: int) -> Tuple[List[Tuple[int, Optional[int]]], float]:
    start = time()
    power_values = []
    for i in range(1, n + 1):
        r = requests.get(url=f"https://pokeapi.co/api/v2/move/{i}/")
        power_values.append((i, r.json()["power"]))
    stop = time()
    return power_values, stop - start


async def main(n: int) -> Tuple[List[Tuple[int, Optional[int]]], float]:
    start = time()
    async with aiohttp.ClientSession("https://pokeapi.co") as session:
        power_values = []

        async def get_value_from_request(session: ClientSession, number: int) -> None:
            async with session.get(f"/api/v2/move/{number}/") as response:
                text = await response.json()
                power_values.append((number, text["power"]))

        asyncio_tasks = []
        for i in range(1, n + 1):
            asyncio_tasks.append(
                asyncio.create_task(get_value_from_request(session, i))
            )

        await asyncio.gather(*asyncio_tasks)
    stop = time()
    return power_values, stop - start


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
_, time_async = asyncio.run(main(100))

_, time_sync = test_request(100)

print(f"sync request time: {time_sync}, async request time: {time_async}")
