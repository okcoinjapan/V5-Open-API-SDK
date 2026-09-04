"""Funding API usage examples.

Demonstrates asset balance retrieval, deposit/withdrawal queries, fund
transfers, and fiat operations.

Run a specific example by uncommenting it in the ``if __name__ == "__main__"``
block at the bottom of this file, then execute:

    python test/funding_test.py
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


# ── Balances ──────────────────────────────────────────────────────────────────

def example_get_balance(client: OkjClient) -> dict:
    """Retrieve the funding account balance for all currencies."""
    return client.funding.get_balance()


def example_get_balance_by_currency(client: OkjClient) -> dict:
    """Retrieve the funding account balance for BTC."""
    return client.funding.get_balance_by_currency(currency="BTC")


# ── Deposits ──────────────────────────────────────────────────────────────────

def example_get_deposit_address(client: OkjClient) -> dict:
    """Retrieve BTC deposit addresses."""
    return client.funding.get_deposit_address(currency="BTC")


def example_get_deposit_history(client: OkjClient) -> dict:
    """Retrieve deposit history for all currencies."""
    return client.funding.get_deposit_history()


def example_get_deposit_history_by_currency(client: OkjClient) -> dict:
    """Retrieve deposit history for BTC only."""
    return client.funding.get_deposit_history_by_currency(currency="BTC")


# ── Withdrawals ───────────────────────────────────────────────────────────────

def example_coin_withdraw(client: OkjClient) -> dict:
    """Submit a PEPE withdrawal request (fill in real values before running)."""
    return client.funding.coin_withdraw(
        currency="PEPE",
        destination="-1",           # destination code; -1 = external address
        amount="10000",
        to_address="your_wallet_address",
        trade_pwd="your_trade_password",
        fee="0",
        chain="PEPE-ERC20",
        reason="your_reason_code",
        usage_agreement="your_usage_agreement",
    )


def example_get_coins_withdraw_record(client: OkjClient) -> dict:
    """Retrieve all recent crypto withdrawal records."""
    return client.funding.get_coins_withdraw_record()


def example_get_coin_withdraw_record(client: OkjClient) -> dict:
    """Retrieve withdrawal records for BTC only."""
    return client.funding.get_coin_withdraw_record(currency="BTC")


# ── Transfers ─────────────────────────────────────────────────────────────────

def example_transfer(client: OkjClient) -> dict:
    """Transfer JPY from the funding account (6) to the trading account (18)."""
    return client.funding.transfer(
        currency="JPY",
        amount="1000",
        account_from=6,
        account_to=18,
    )


# ── Ledger ────────────────────────────────────────────────────────────────────

def example_get_ledger_record(client: OkjClient) -> dict:
    """Retrieve asset ledger records for JPY, limited to 2 entries."""
    return client.funding.get_ledger_record(currency="JPY", limit="2")


# ── Currencies ────────────────────────────────────────────────────────────────

def example_get_currencies(client: OkjClient) -> dict:
    """Retrieve the list of all supported currencies."""
    return client.funding.get_currencies()


# ── Fiat ─────────────────────────────────────────────────────────────────────

def example_get_bank_card(client: OkjClient) -> dict:
    """Retrieve the list of registered bank cards."""
    return client.funding.get_bank_card()


def example_fiat_withdraw(client: OkjClient) -> dict:
    """Submit a fiat (JPY) withdrawal to a bank card (fill in real values)."""
    return client.funding.fiat_withdraw(
        amount="10000",
        trade_pwd="your_trade_password",
        bank_card_id="your_bank_card_id",
    )


def example_fiat_withdraw_history(client: OkjClient) -> dict:
    """Retrieve fiat withdrawal history."""
    return client.funding.fiat_withdraw_history()


def example_fiat_deposit_history(client: OkjClient) -> dict:
    """Retrieve fiat deposit history."""
    return client.funding.fiat_deposit_history()


# ── Asset valuation & fees ────────────────────────────────────────────────────

def example_get_asset_valuation(client: OkjClient) -> dict:
    """Retrieve the total asset valuation of the account."""
    return client.funding.get_asset_valuation()


def example_get_coin_fee(client: OkjClient) -> dict:
    """Retrieve withdrawal fees for BTC."""
    return client.funding.get_coin_fee(currency="BTC")


if __name__ == "__main__":
    import json

    client = get_client()

    # Uncomment the example you want to run:

    # print(json.dumps(example_get_balance(client), indent=2, ensure_ascii=False))
    # print(json.dumps(example_get_balance_by_currency(client), indent=2, ensure_ascii=False))
    # print(json.dumps(example_get_deposit_address(client), indent=2, ensure_ascii=False))
    # print(json.dumps(example_get_deposit_history(client), indent=2, ensure_ascii=False))
    # print(json.dumps(example_get_coins_withdraw_record(client), indent=2, ensure_ascii=False))
    # print(json.dumps(example_get_currencies(client), indent=2, ensure_ascii=False))
    # print(json.dumps(example_get_bank_card(client), indent=2, ensure_ascii=False))
    # print(json.dumps(example_get_asset_valuation(client), indent=2, ensure_ascii=False))
    # print(json.dumps(example_get_coin_fee(client), indent=2, ensure_ascii=False))

    client.close()
