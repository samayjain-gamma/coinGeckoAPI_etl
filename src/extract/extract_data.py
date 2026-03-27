import requests
import logging

API_URL = "https://api.coingecko.com/api/v3/coins/markets"


def fetch_top_50_cryptos():
    '''
    will fetch the data of top 50 crypto currencies
    
    '''

    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1
    }

    try:
        logging.info("Fetching crypto data from CoinGecko API")

        response = requests.get(API_URL, params=params, timeout=12)

        response.raise_for_status()

        data = response.json()

        logging.info(f"Fetched {len(data)} records")

        return data

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        raise


if __name__ == "__main__":

    data = fetch_top_50_cryptos()

    print(len(data))
    print(type(data))
    # print(data[0])
    for i in range(1):
        print("\n" *3)
        for key, value in data[i].items():
            print(f"{key}: {value}")