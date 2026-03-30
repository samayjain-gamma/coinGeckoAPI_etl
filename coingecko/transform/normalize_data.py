import logging

from coingecko.extract.extract_data import fetch_top_50_cryptos
from coingecko.transform.clean_data import clean_crypto_data


def normalize_crypto_data(clean_data):
    """
    converting cleaned data
    cleaned data -> returned form src.transform.clean_data clean_crypto_data
    into
    normalized one
    so that it can be direclty stored in db
    """

    coins = []
    prices = []
    market_data = []

    for coin in clean_data:

        coin_id = coin["id"]

        coins.append({"coin_id": coin_id, "name": coin.get("name")})

        prices.append(
            {
                "coin_id": coin_id,
                "price": coin.get("price"),
                "last_updated": coin.get("last_updated"),
            }
        )

        market_data.append(
            {
                "coin_id": coin_id,
                "market_cap": coin.get("market_cap"),
                "total_volume": coin.get("volume"),
                "market_cap_rank": coin.get("rank"),
            }
        )

    logging.info(
        f"Normalized records -> coins:{len(coins)}, "
        f"prices:{len(prices)}, market_data:{len(market_data)}"
    )

    return {"coins": coins, "prices": prices, "market_data": market_data}


if __name__ == "__main__":

    data = fetch_top_50_cryptos()
    print(f"lenght of data : {len(data)}")
    print(data[0])
    cleaned_data = clean_crypto_data(data)

    print(len(cleaned_data))
    print(cleaned_data[0])

    normalized_data = normalize_crypto_data(clean_data=cleaned_data)

    print(f"type of normalized data : {type(normalized_data)}")

    for i in range(2):
        print(normalized_data.get("coins")[i])
        print(normalized_data.get("prices")[i])
        print(normalized_data.get("market_data")[i])
