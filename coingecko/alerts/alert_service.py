import asyncio

from coingecko.alerts.mail_service import send_email
from coingecko.extract.extract_data import fetch_top_50_cryptos
from coingecko.load.load_to_db import load_to_db
from coingecko.transform.clean_data import clean_crypto_data
from coingecko.transform.normalize_data import normalize_crypto_data


def process_prize_alert(alerts):
    """
    receieve alerts data from load_data
    will send alert
    """

    if not alerts:
        print("No alerts detected")
        return

    subject = "Crypto Price Alert"

    lines = []

    for alert in alerts:

        coin = alert["coin_id"]
        old_price = alert["old_price"]
        new_price = alert["new_price"]
        change = alert["change"] * 100

        line = (
            f"Coin: {coin}\n"
            f"Old Price: {old_price}\n"
            f"New Price: {new_price}\n"
            f"Change: {change:.2f}%\n"
        )

        lines.append(line)

    body = "\n---------------------\n".join(lines)

    send_email(to_email="samay.jain@gammaedge.io", subject=subject, body=body)


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

    alerts = data_loaded
    print(f"Object type of alert : f{type(alerts)}")
    print(f"Number of alerts : {len(alerts)}")
    process_prize_alert(alerts=alerts)

    # print(f"Number of alerts : {len(data_loaded['alerts'])} ")
