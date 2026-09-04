"""Funding API — asset balances, deposits, withdrawals, and fiat operations.

Accessed via ``client.funding`` on an :class:`okj.OkjClient` instance.

Endpoint paths live in :mod:`okj.consts`. OKJ's funding domain is a separate
implementation from OKX's and uses nested paths, and every path in this module
was wrong until 2026-08-28 because it was written from OKX's docs.
"""

from __future__ import annotations

from .._http import _HttpClient
from .. import consts as c


class FundingAPI:
    """Provides access to the OKJ Funding / Asset REST endpoints.

    Do not instantiate directly; use :class:`okj.OkjClient` instead::

        client = OkjClient(api_key="...", api_secret_key="...", passphrase="...")
        balance = client.funding.get_balance()
    """

    def __init__(self, http: _HttpClient) -> None:
        self._http = http

    # ── Balances ──────────────────────────────────────────────────────────────

    def get_balance(self) -> dict:
        """Retrieve the funding account balance for all currencies.

        Returns:
            Parsed API response dict.
        """
        return self._http.get(c.GET_BALANCES)

    def get_balance_by_currency(self, currency: str) -> dict:
        """Retrieve the funding account balance for a specific currency.

        Args:
            currency: Currency code, e.g. ``"BTC"``.

        Returns:
            Parsed API response dict.
        """
        return self._http.get(f"{c.GET_BALANCES}/{currency}")

    # ── Deposit ───────────────────────────────────────────────────────────────

    def get_deposit_address(self, currency: str) -> dict:
        """Retrieve deposit addresses for a currency.

        Args:
            currency: Currency code, e.g. ``"BTC"``.

        Returns:
            Parsed API response dict.
        """
        params = {"currency": currency}
        return self._http.get(c.DEPOSIT_ADDRESS, params)

    def get_deposit_history(self) -> dict:
        """Retrieve the deposit history for all currencies.

        Returns:
            Parsed API response dict.
        """
        return self._http.get(c.DEPOSIT_HISTORY)

    def get_deposit_history_by_currency(self, currency: str) -> dict:
        """Retrieve the deposit history for a specific currency.

        Args:
            currency: Currency code, e.g. ``"BTC"``.

        Returns:
            Parsed API response dict.
        """
        return self._http.get(f"{c.DEPOSIT_HISTORY}/{currency}")

    # ── Withdrawal ────────────────────────────────────────────────────────────

    def coin_withdraw(
        self,
        currency: str,
        destination: str,
        amount: str,
        to_address: str,
        trade_pwd: str,
        fee: str,
        chain: str,
        reason: str,
        usage_agreement: str,
    ) -> dict:
        """Submit a crypto withdrawal request.

        Args:
            currency:        Currency code, e.g. ``"BTC"``.
            destination:     Withdrawal destination code.
            amount:          Withdrawal amount.
            to_address:      Destination wallet address.
            trade_pwd:       Trading password for verification.
            fee:             Network fee.
            chain:           Blockchain network, e.g. ``"BTC-Bitcoin"``.
            reason:          Reason code for the withdrawal.
            usage_agreement: Usage agreement acceptance flag.

        Returns:
            Parsed API response dict.
        """
        params = {
            "currency": currency, "amount": amount, "destination": destination,
            "to_address": to_address, "trade_pwd": trade_pwd, "fee": fee,
            "chain": chain, "reason": reason, "usage_agreement": usage_agreement,
        }
        return self._http.post(c.WITHDRAWAL_COIN, params)

    def get_coins_withdraw_record(self) -> dict:
        """Retrieve all recent crypto withdrawal records.

        Returns:
            Parsed API response dict.
        """
        return self._http.get(c.WITHDRAWAL_HISTORY)

    def get_coin_withdraw_record(self, currency: str) -> dict:
        """Retrieve withdrawal records for a specific currency.

        Args:
            currency: Currency code, e.g. ``"BTC"``.

        Returns:
            Parsed API response dict.
        """
        return self._http.get(f"{c.WITHDRAWAL_HISTORY}/{currency}")

    # ── Transfer ──────────────────────────────────────────────────────────────

    def transfer(
        self,
        currency: str,
        amount: str,
        account_from: int,
        account_to: int,
    ) -> dict:
        """Transfer assets between accounts.

        Args:
            currency:     Currency code.
            amount:       Transfer amount.
            account_from: Source account type code.
            account_to:   Destination account type code.

        Returns:
            Parsed API response dict.
        """
        params = {
            "currency": currency, "amount": amount,
            "from": account_from, "to": account_to,
        }
        return self._http.post(c.FUNDS_TRANSFER, params)

    # ── Ledger ────────────────────────────────────────────────────────────────

    def get_ledger_record(
        self,
        *,
        currency: str = "",
        after: str = "",
        before: str = "",
        limit: str = "",
        type: str = "",
    ) -> dict:
        """Retrieve asset ledger (bill) records.

        Args:
            currency: Currency filter.
            type:     Bill type filter.
            limit:    Number of records to return.

        Returns:
            Parsed API response dict.
        """
        params = {"after": after, "before": before, "limit": limit, "type": type}
        if currency:
            params["currency"] = currency
        return self._http.get(c.LEDGER_RECORD, params)

    # ── Currencies ────────────────────────────────────────────────────────────

    def get_currencies(self) -> dict:
        """Retrieve the list of all supported currencies.

        Returns:
            Parsed API response dict.
        """
        return self._http.get(c.CURRENCY_INFO)

    # ── Fiat operations ───────────────────────────────────────────────────────

    def get_bank_card(self) -> dict:
        """Retrieve the list of registered bank cards.

        Returns:
            Parsed API response dict.
        """
        return self._http.get(c.BANK_CARD_LIST)

    def fiat_withdraw(
        self,
        amount: str,
        trade_pwd: str,
        bank_card_id: str,
    ) -> dict:
        """Submit a fiat (JPY) withdrawal request.

        Args:
            amount:       Withdrawal amount.
            trade_pwd:    Trading password for verification.
            bank_card_id: Target bank card ID.

        Returns:
            Parsed API response dict.
        """
        params = {"amount": amount, "trade_pwd": trade_pwd, "bank_card_id": bank_card_id}
        return self._http.post(c.FIAT_WITHDRAW, params)

    def fiat_withdraw_history(self) -> dict:
        """Retrieve fiat withdrawal history.

        Returns:
            Parsed API response dict.
        """
        return self._http.get(c.FIAT_WITHDRAW_RECORD)

    def fiat_deposit_history(self) -> dict:
        """Retrieve fiat deposit history.

        Returns:
            Parsed API response dict.
        """
        return self._http.get(c.FIAT_DEPOSIT_RECORD)

    # ── Asset valuation & fees ────────────────────────────────────────────────

    def get_asset_valuation(self, *, account_type: str = "") -> dict:
        """Retrieve the total asset valuation of the account.

        Args:
            account_type: Account type filter (optional).

        Returns:
            Parsed API response dict.
        """
        params = {}
        if account_type:
            params["account_type"] = account_type
        return self._http.get(c.ASSET_VALUATION, params)

    def get_coin_fee(self, *, currency: str = "") -> dict:
        """Retrieve withdrawal fees for a currency.

        Args:
            currency: Currency code.  When omitted, returns fees for all
                      supported currencies.

        Returns:
            Parsed API response dict.
        """
        params = {}
        if currency:
            params["currency"] = currency
        return self._http.get(c.COIN_FEE, params)
