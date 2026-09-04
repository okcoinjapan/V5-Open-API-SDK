"""Account API — balance, bills, configuration, and fee rates.

Accessed via ``client.account`` on an :class:`okj.OkjClient` instance.
"""

from __future__ import annotations

from .._http import _HttpClient
from .. import consts as c


class AccountAPI:
    """Provides access to the OKJ Account REST endpoints.

    Do not instantiate directly; use :class:`okj.OkjClient` instead::

        client = OkjClient(api_key="...", api_secret_key="...", passphrase="...")
        balance = client.account.get_account_balance()
    """

    def __init__(self, http: _HttpClient) -> None:
        self._http = http

    # ── Balance & Bills ───────────────────────────────────────────────────────

    def get_account_balance(self, *, ccy: str = "") -> dict:
        """Retrieve account balance.

        Args:
            ccy: Optional currency filter (e.g. ``"BTC"``).  When omitted,
                 returns balances for all currencies.

        Returns:
            Parsed API response dict.
        """
        params = {}
        if ccy:
            params["ccy"] = ccy
        return self._http.get(c.ACCOUNT_INFO, params)

    def get_account_bills(
        self,
        *,
        inst_type: str = "",
        inst_id: str = "",
        ccy: str = "",
        type: str = "",
        sub_type: str = "",
        after: str = "",
        before: str = "",
        limit: str = "",
        begin: str = "",
        end: str = "",
    ) -> dict:
        """Retrieve account bill details from the last 7 days.

        Args:
            inst_type: Instrument type filter (e.g. ``"SPOT"``).
            ccy:       Currency filter.
            type:      Bill type filter.

        Returns:
            Parsed API response dict.
        """
        params = {
            "instType": inst_type, "ccy": ccy, "instId": inst_id, "type": type,
            "subType": sub_type, "after": after, "before": before,
            "limit": limit, "begin": begin, "end": end,
        }
        return self._http.get(c.BILLS_DETAIL, params)

    def get_account_bills_archive(
        self,
        *,
        inst_type: str = "",
        inst_id: str = "",
        ccy: str = "",
        type: str = "",
        sub_type: str = "",
        after: str = "",
        before: str = "",
        limit: str = "",
        begin: str = "",
        end: str = "",
    ) -> dict:
        """Retrieve account bill details from the last 3 months.

        Returns:
            Parsed API response dict.
        """
        params = {
            "instType": inst_type, "ccy": ccy, "instId": inst_id, "type": type,
            "subType": sub_type, "after": after, "before": before,
            "limit": limit, "begin": begin, "end": end,
        }
        return self._http.get(c.BILLS_ARCHIVE, params)

    # ── Configuration ─────────────────────────────────────────────────────────

    def get_account_config(self) -> dict:
        """Retrieve the current account configuration.

        Returns:
            Parsed API response dict containing account settings such as
            ``posMode``, ``acctLv``, and ``uid``.
        """
        return self._http.get(c.ACCOUNT_CONFIG)

    # ── Trading size & limits ─────────────────────────────────────────────────

    def get_max_order_size(self, inst_id: str, td_mode: str) -> dict:
        """Retrieve the maximum tradable size for an instrument.

        Args:
            inst_id: Instrument ID, e.g. ``"BTC-JPY"``.
            td_mode: Trade mode — ``"cash"`` for spot.

        Returns:
            Parsed API response dict.
        """
        params = {"instId": inst_id, "tdMode": td_mode}
        return self._http.get(c.MAX_TRADE_SIZE, params)

    def get_max_avail_size(self, inst_id: str, td_mode: str) -> dict:
        """Retrieve the maximum available tradable amount for an instrument.

        Args:
            inst_id: Instrument ID.
            td_mode: Trade mode.

        Returns:
            Parsed API response dict.
        """
        params = {"instId": inst_id, "tdMode": td_mode}
        return self._http.get(c.MAX_AVAIL_SIZE, params)

    def get_max_withdrawal(self, *, ccy: str = "") -> dict:
        """Retrieve the maximum withdrawal amount.

        Args:
            ccy: Currency to query.  When omitted, returns all currencies.

        Returns:
            Parsed API response dict.
        """
        params = {}
        if ccy:
            params["ccy"] = ccy
        return self._http.get(c.MAX_WITHDRAWAL, params)

    # ── Instruments & Fees ────────────────────────────────────────────────────

    def get_instruments(self, *, inst_type: str = "", inst_id: str = "") -> dict:
        """Retrieve tradable instruments available to the account.

        Args:
            inst_type: Instrument type filter (e.g. ``"SPOT"``).
            inst_id:   Instrument ID filter.

        Returns:
            Parsed API response dict.
        """
        params = {"instType": inst_type, "instId": inst_id}
        return self._http.get(c.GET_INSTRUMENTS, params)

    def get_fee_rates(self, inst_type: str, *, inst_id: str = "") -> dict:
        """Retrieve fee rates for an instrument type.

        Args:
            inst_type: Instrument type (e.g. ``"SPOT"``).
            inst_id:   Instrument ID for product-specific rates.

        Returns:
            Parsed API response dict.
        """
        params = {"instType": inst_type, "instId": inst_id}
        return self._http.get(c.FEE_RATES, params)

    def get_fee_rates_all(self, inst_type: str) -> dict:
        """Retrieve fee rates for all tiers of an instrument type.

        Args:
            inst_type: Instrument type (e.g. ``"SPOT"``).

        Returns:
            Parsed API response dict.
        """
        params = {"instType": inst_type}
        return self._http.get(c.FEE_RATES_ALL, params)
