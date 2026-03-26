CoinGecko Crypto Price Pipeline - It's free, no auth required for basic use, has clean JSON responses, and includes multiple data points (price, volume, market cap). The task would be:
 Fetch top 50 cryptocurrencies every hour
 Clean/validate the data (handle nulls, outliers)
 Transform into normalized tables (coins, prices, market_data)
 Load into PostgreSQL/MySQL with proper indexing
 Add error handling and logging
 Create a simple alerting mechanism for major price changes