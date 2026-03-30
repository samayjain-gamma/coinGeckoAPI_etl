import asyncio

from coingecko.utils.base import Base
from coingecko.utils.db import engine
from coingecko.utils.models import Coin, MarketData, Price


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_models())
