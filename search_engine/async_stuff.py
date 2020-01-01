import asyncio
from aiohttp import ClientSession
from timeit import timeit


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read()


async def run(urls):
    # Delay to make sure we don`t have all connections at the same time
    delay = 0.15
    tasks = []
    # Create client session that will ensure we don't open new connection per each request.
    async with ClientSession() as session:
        # Pass first get
        task = asyncio.ensure_future(fetch(urls[0], session))
        tasks.append(task)

        # Pass other links with delay
        for url in urls[1:]:
            await asyncio.sleep(delay)
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        return responses


def scrap_web_pages(urls):
    print('we here')
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(urls))
    print('and here')
    result = loop.run_until_complete(future)
    return result
