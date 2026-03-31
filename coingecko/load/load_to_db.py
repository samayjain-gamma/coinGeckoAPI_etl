import asyncio

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from coingecko.extract.extract_data import fetch_top_50_cryptos
from coingecko.transform.clean_data import clean_crypto_data
from coingecko.transform.normalize_data import normalize_crypto_data
from coingecko.utils.db import SessionLocal
from coingecko.utils.models import Coin, MarketData, Price

PRICE_ALERT_THRESHOLD = 0.001


async def load_to_db(normalized_data):
    """
    load normalized data
    returned from normalize_crypto_data

    performs:
        upsert on coins
        price change detection and store into alerts[]
        upsert on prices
        upsert on Maerket_data
    """

    coins = normalized_data["coins"]
    prices = normalized_data["prices"]
    market_data = normalized_data["market_data"]

    alerts = []

    async with SessionLocal() as session:

        if coins:

            query = insert(Coin).values(coins)

            query = query.on_conflict_do_update(
                index_elements=["coin_id"], set_={"name": query.excluded.name}
            )

            await session.execute(query)

        for row in prices:

            coin_id = row["coin_id"]
            new_price = row["price"]

            result = await session.execute(
                select(Price.price).where(Price.coin_id == coin_id)
            )

            old_price = result.scalar()

            if old_price is not None:

                change = (new_price - old_price) / old_price

                if abs(change) > PRICE_ALERT_THRESHOLD:

                    alerts.append(
                        {
                            "coin_id": coin_id,
                            "old_price": old_price,
                            "new_price": new_price,
                            "change": change,
                        }
                    )

        if prices:

            query = insert(Price).values(prices)

            query = query.on_conflict_do_update(
                index_elements=["coin_id"],
                set_={
                    "price": query.excluded.price,
                    "last_updated": query.excluded.last_updated,
                },
            )

            await session.execute(query)

        if market_data:

            query = insert(MarketData).values(market_data)

            query = query.on_conflict_do_update(
                index_elements=["coin_id"],
                set_={
                    "market_cap": query.excluded.market_cap,
                    "total_volume": query.excluded.total_volume,
                    "market_cap_rank": query.excluded.market_cap_rank,
                },
            )

            await session.execute(query)

        await session.commit()

    return alerts


if __name__ == "__main__":
    data = fetch_top_50_cryptos()
    print(f"lenght of data : {len(data)}")
    print(data[0])
    cleaned_data = clean_crypto_data(data)

    print(len(cleaned_data))
    print(cleaned_data[0])

    normalized_data = normalize_crypto_data(clean_data=cleaned_data)

    print(
        f'Noremalized data : \n{normalized_data.get("coins")[0]} \n{normalized_data.get("prices")[0]}\n{normalized_data.get("market_data")[0]}'
    )

    data_loaded = asyncio.run(load_to_db(normalized_data))

    print("data loaded")

    print(f"\nType of data returned : {type(data_loaded)}")
    print(f'alert : {data_loaded["alerts"]}')
    # print(f'alert : {data_loaded["alerts"]}')
    print(f"Number of alerts : {len(data_loaded['alerts'])} ")
