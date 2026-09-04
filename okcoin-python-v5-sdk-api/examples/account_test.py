"""Account API usage examples.

Demonstrates balance retrieval, account configuration, fee rates, and
bill history.

Run a specific example by uncommenting it in the ``if __name__ == "__main__"``
block at the bottom of this file, then execute:

    python test/account_test.py
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


def example_get_account_balance(client: OkjClient) -> dict:
    """Retrieve balance for all currencies."""
    return client.account.get_account_balance()


def example_get_account_balance_by_currency(client: OkjClient) -> dict:
    """Retrieve balance for a specific currency."""
    return client.account.get_account_balance(ccy="BTC")


def example_get_account_bills(client: OkjClient) -> dict:
    """Retrieve account bills from the last 7 days."""
    return client.account.get_account_bills(inst_type="SPOT", limit="20")


def example_get_account_bills_archive(client: OkjClient) -> dict:
    """Retrieve account bills from the last 3 months."""
    return client.account.get_account_bills_archive(inst_type="SPOT")


def example_get_account_config(client: OkjClient) -> dict:
    """Retrieve current account configuration (position mode, account level, etc.)."""
    return client.account.get_account_config()


def example_get_max_order_size(client: OkjClient) -> dict:
    """Retrieve the maximum tradable size for BTC-JPY spot."""
    return client.account.get_max_order_size(inst_id="BTC-JPY", td_mode="cash")


def example_get_max_avail_size(client: OkjClient) -> dict:
    """Retrieve the maximum available tradable amount for BTC-JPY spot."""
    return client.account.get_max_avail_size(inst_id="BTC-JPY", td_mode="cash")


def example_get_max_withdrawal(client: OkjClient) -> dict:
    """Retrieve the maximum withdrawal amount for all currencies."""
    return client.account.get_max_withdrawal()


def example_get_instruments(client: OkjClient) -> dict:
    """Retrieve all SPOT instruments available to the account."""
    return client.account.get_instruments(inst_type="SPOT")


def example_get_fee_rates(client: OkjClient) -> dict:
    """Retrieve fee rates for SPOT trading."""
    return client.account.get_fee_rates(inst_type="SPOT")


def example_get_fee_rates_all(client: OkjClient) -> dict:
    """Retrieve fee rates for all tiers of SPOT trading."""
    return client.account.get_fee_rates_all(inst_type="SPOT")


if __name__ == "__main__":
    import json

    client = get_client()

    # Uncomment the example you want to run:

    # print(json.dumps(example_get_account_balance(client), indent=2, ensure_ascii=False))
    # print(json.dumps(example_get_account_balance_by_currency(client), indent=2, ensure_ascii=False))
    # print(json.dumps(example_get_account_config(client), indent=2, ensure_ascii=False))
    # print(json.dumps(example_get_account_bills(client), indent=2, ensure_ascii=False))
    # print(json.dumps(example_get_fee_rates(client), indent=2, ensure_ascii=False))
    # print(json.dumps(example_get_instruments(client), indent=2, ensure_ascii=False))

    client.close()
