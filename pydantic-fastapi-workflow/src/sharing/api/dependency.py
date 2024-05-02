from edgedb import create_async_client


async def get_client():
    async with create_async_client() as client:
        yield client
