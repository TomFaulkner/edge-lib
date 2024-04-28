from ..db import client_context


async def edge_tx():
    async with client_context() as client:
        async for tx in client.transaction():
            async with tx:
                yield tx
