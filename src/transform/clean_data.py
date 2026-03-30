import logging

from src.extract.extract_data import fetch_top_50_cryptos


def clean_crypto_data(raw_data):
    """
    clean the dat a  get from src/extract/extract_data fetfch_top_50
    """

    cleaned_data = []
    seen_coins = set()

    for coin in raw_data:

        coin_id = coin.get("id")
        symbol = coin.get("symbol")
        price = coin.get("current_price")

        if not coin_id or not symbol or price is None:
            logging.warning(f"Skipping record due to missing fields: {coin}")
            continue

        if coin_id in seen_coins:
            logging.warning(f"Duplicate coin detected: {coin_id}")
            continue

        seen_coins.add(coin_id)

        try:
            price = float(price)
            market_cap = float(coin.get("market_cap", 0))
            volume = float(coin.get("total_volume", 0))
            rank = int(coin.get("market_cap_rank", 0))

        except (ValueError, TypeError):
            logging.warning(f"Type conversion failed for coin: {coin_id}")
            continue

        if price <= 0:
            logging.warning(f"Invalid price for coin: {coin_id}")
            continue

        if market_cap < 0 or volume < 0:
            logging.warning(f"Invalid market data for coin: {coin_id}")
            continue

        cleaned_record = {
            "id": coin_id,
            "name": coin.get("name"),
            "price": price,
            "market_cap": market_cap,
            "volume": volume,
            "rank": rank,
            "last_updated": coin.get("last_updated"),
        }

        cleaned_data.append(cleaned_record)

    logging.info(f"Cleaned dataset size: {len(cleaned_data)}")

    return cleaned_data


print("hello")

if __name__ == "__main__":
    data = fetch_top_50_cryptos()
    print(f"lenght of data : {len(data)}")
    print(data[0])
    cleaned_data = clean_crypto_data(data)

    print(type(cleaned_data))
    print(len(cleaned_data))
    print(cleaned_data[0])

    pass
