"""Market Data API usage examples.

Demonstrates ticker retrieval, order book queries, candlestick data,
and trade history — all public endpoints requiring no authentication.

Run a specific example by uncommenting it in the ``if __name__ == "__main__"``
block at the bottom of this file, then execute:

    python test/market_test.py
"""

from okj import OkjClient
from api_config import DOMAIN


def get_client() -> OkjClient:
    # Market data endpoints are public — no API credentials required.
    return OkjClient(base_url=DOMAIN)


def example_get_tickers(client: OkjClient) -> dict:
    """Retrieve ticker data for all SPOT instruments."""
    return client.market.get_tickers(inst_type="SPOT")


def example_get_ticker(client: OkjClient) -> dict:
    """Retrieve ticker data for BTC-JPY."""
    return client.market.get_ticker(inst_id="BTC-JPY")


def example_get_orderbook(client: OkjClient) -> dict:
    """Retrieve the top 20 levels of the BTC-JPY order book."""
    return client.market.get_orderbook(inst_id="BTC-JPY", sz="20")


def example_get_orderbook_full(client: OkjClient) -> dict:
    """Retrieve the full order book for BTC-JPY."""
    return client.market.get_orderbook_full(inst_id="BTC-JPY")


def example_get_candlesticks(client: OkjClient) -> dict:
    """Retrieve the last 100 one-minute candles for BTC-JPY."""
    return client.market.get_candlesticks(inst_id="BTC-JPY", bar="1m", limit="100")


def example_get_history_candlesticks(client: OkjClient) -> dict:
    """Retrieve historical daily candles for BTC-JPY."""
    return client.market.get_history_candlesticks(inst_id="BTC-JPY", bar="1D", limit="30")


def example_get_trades(client: OkjClient) -> dict:
    """Retrieve the 50 most recent trades for BTC-JPY."""
    return client.market.get_trades(inst_id="BTC-JPY", limit="50")


def example_get_volume(client: OkjClient) -> dict:
    """Retrieve the platform's 24-hour trading volume."""
    return client.market.get_volume()


def example_get_call_auction_details(client: OkjClient) -> dict:
    """Retrieve call auction details for BTC-JPY."""
    return client.market.get_call_auction_details(inst_id="BTC-JPY")


if __name__ == "__main__":
    import json

    client = get_client()

    # Uncomment the example you want to run:

    # print(json.dumps(example_get_tickers(client), indent=2, ensure_ascii=False))
    # print(json.dumps(example_get_ticker(client), indent=2, ensure_ascii=False))
    # print(json.dumps(example_get_orderbook(client), indent=2, ensure_ascii=False))
    # print(json.dumps(example_get_candlesticks(client), indent=2, ensure_ascii=False))
    # print(json.dumps(example_get_trades(client), indent=2, ensure_ascii=False))
    # print(json.dumps(example_get_volume(client), indent=2, ensure_ascii=False))

    client.close()
