"""Trade API usage examples.

Demonstrates order placement, cancellation, amendment, and history retrieval.

Run a specific example by uncommenting it in the ``if __name__ == "__main__"``
block at the bottom of this file, then execute:

    python test/trade_test.py
"""

from okj import OkjClient
from api_config import API_KEY, API_SECRET_KEY, PASSPHRASE, DOMAIN


def get_client() -> OkjClient:
    return OkjClient(
        api_key=API_KEY,
        api_secret_key=API_SECRET_KEY,
        passphrase=PASSPHRASE,
        base_url=DOMAIN,
    )


# ── Standard orders ───────────────────────────────────────────────────────────

def example_place_order(client: OkjClient) -> dict:
    """Place a limit buy order."""
    return client.trade.place_order(
        inst_id="BTC-JPY",
        td_mode="cash",
        side="buy",
        ord_type="limit",
        sz="0.001",
        px="5000000",
    )


def example_place_multiple_orders(client: OkjClient) -> dict:
    """Place multiple orders in a single batch request."""
    return client.trade.place_multiple_orders([
        {"instId": "ETH-JPY", "tdMode": "cash", "side": "buy", "ordType": "limit", "sz": "0.01", "px": "300000"},
        {"instId": "BTC-JPY", "tdMode": "cash", "side": "buy", "ordType": "limit", "sz": "0.001", "px": "5000000"},
    ])


def example_cancel_order(client: OkjClient, ord_id: str) -> dict:
    """Cancel an order by its exchange-assigned order ID."""
    return client.trade.cancel_order(inst_id="BTC-JPY", ord_id=ord_id)


def example_cancel_multiple_orders(client: OkjClient) -> dict:
    """Cancel multiple orders in a single batch request."""
    return client.trade.cancel_multiple_orders([
        {"instId": "ETH-JPY", "ordId": "order_id_1"},
        {"instId": "ETH-JPY", "ordId": "order_id_2"},
    ])


def example_amend_order(client: OkjClient, ord_id: str) -> dict:
    """Amend the price and size of an existing order."""
    return client.trade.amend_order(
        inst_id="BTC-JPY",
        ord_id=ord_id,
        new_sz="0.002",
        new_px="4900000",
    )


def example_amend_multiple_orders(client: OkjClient) -> dict:
    """Amend multiple orders in a single batch request."""
    return client.trade.amend_multiple_orders([
        {"instId": "ETH-JPY", "ordId": "order_id_1", "newSz": "0.02"},
        {"instId": "ETH-JPY", "ordId": "order_id_2", "newSz": "0.03"},
    ])


# ── Order queries ─────────────────────────────────────────────────────────────

def example_get_order(client: OkjClient, ord_id: str) -> dict:
    """Retrieve details of a specific order."""
    return client.trade.get_order(inst_id="BTC-JPY", ord_id=ord_id)


def example_get_order_by_client_id(client: OkjClient, cl_ord_id: str) -> dict:
    """Retrieve an order by client-assigned order ID."""
    return client.trade.get_order(inst_id="BTC-JPY", cl_ord_id=cl_ord_id)


def example_get_order_list(client: OkjClient) -> dict:
    """Retrieve all pending (unfilled) orders."""
    return client.trade.get_order_list()


def example_get_orders_history(client: OkjClient) -> dict:
    """Retrieve order history from the last 7 days."""
    return client.trade.get_orders_history(inst_type="SPOT")


def example_get_orders_history_archive(client: OkjClient) -> dict:
    """Retrieve order history from the last 3 months (canceled orders)."""
    return client.trade.get_orders_history_archive(inst_type="SPOT", state="canceled")


def example_get_fills(client: OkjClient) -> dict:
    """Retrieve transaction details from the last 3 days."""
    return client.trade.get_fills()


def example_get_fills_history(client: OkjClient) -> dict:
    """Retrieve transaction details from the last 30 days."""
    return client.trade.get_fills_history(inst_type="SPOT", limit="10")


def example_cancel_all_orders(client: OkjClient) -> dict:
    """Schedule cancellation of all open orders after 10 seconds."""
    return client.trade.cancel_all_orders(time_out="10")


# ── Algo orders ───────────────────────────────────────────────────────────────

def example_place_algo_order(client: OkjClient) -> dict:
    """Place a conditional (stop-loss) algo order."""
    return client.trade.place_algo_order(
        inst_id="BTC-JPY",
        td_mode="cash",
        side="sell",
        ord_type="conditional",
        sz="0.001",
        sl_trigger_px="4000000",
        sl_ord_px="-1",  # market price on trigger
    )


def example_cancel_algo_order(client: OkjClient, algo_id: str) -> dict:
    """Cancel a single algo order."""
    return client.trade.cancel_algo_order(algo_id=algo_id, inst_id="BTC-JPY")


def example_cancel_multiple_algo_orders(client: OkjClient) -> dict:
    """Cancel multiple algo orders in a single batch request."""
    return client.trade.cancel_multiple_algo_orders([
        {"algoId": "algo_id_1", "instId": "BTC-JPY"},
        {"algoId": "algo_id_2", "instId": "BTC-JPY"},
    ])


def example_get_algo_order_details(client: OkjClient, algo_id: str) -> dict:
    """Retrieve details of a specific algo order."""
    return client.trade.get_algo_order_details(algo_id=algo_id)


def example_get_algo_order_list(client: OkjClient) -> dict:
    """Retrieve pending algo orders (conditional and OCO types)."""
    return client.trade.get_algo_order_list(ord_type="conditional,oco", inst_type="SPOT")


def example_get_algo_order_history(client: OkjClient) -> dict:
    """Retrieve historical algo orders."""
    return client.trade.get_algo_order_history(
        ord_type="conditional",
        inst_type="SPOT",
        state="canceled",
        limit="10",
    )


def example_amend_algo_order(client: OkjClient, algo_id: str) -> dict:
    """Amend the stop-loss trigger price of an algo order."""
    return client.trade.amend_algo_order(
        inst_id="BTC-JPY",
        algo_id=algo_id,
        new_sl_trigger_px="3800000",
        new_sl_ord_px="-1",
    )


if __name__ == "__main__":
    import json

    client = get_client()

    # Uncomment the example you want to run:

    # print(json.dumps(example_place_order(client), indent=2, ensure_ascii=False))
    # print(json.dumps(example_place_multiple_orders(client), indent=2, ensure_ascii=False))
    # print(json.dumps(example_cancel_order(client, ord_id="your_ord_id"), indent=2, ensure_ascii=False))
    # print(json.dumps(example_get_order_list(client), indent=2, ensure_ascii=False))
    # print(json.dumps(example_get_orders_history(client), indent=2, ensure_ascii=False))
    # print(json.dumps(example_get_fills(client), indent=2, ensure_ascii=False))
    # print(json.dumps(example_place_algo_order(client), indent=2, ensure_ascii=False))

    client.close()
