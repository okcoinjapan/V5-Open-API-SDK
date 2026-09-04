"""Market Data API — tickers, order books, candles, and trades.

Accessed via ``client.market`` on an :class:`okj.OkjClient` instance.
"""

from __future__ import annotations

from .._http import _HttpClient
from .. import consts as c


class MarketAPI:
    """Provides access to the OKJ Market Data REST endpoints.

    Do not instantiate directly; use :class:`okj.OkjClient` instead::

        client = OkjClient(api_key="...", api_secret_key="...", passphrase="...")
        ticker = client.market.get_ticker(inst_id="BTC-JPY")
    """

    def __init__(self, http: _HttpClient) -> None:
        self._http = http

    # ── Tickers ───────────────────────────────────────────────────────────────

    def get_tickers(self, inst_type: str) -> dict:
        """Retrieve ticker data for all instruments of a given type.

        Args:
            inst_type: Instrument type — ``"SPOT"``, ``"FUTURES"``, etc.

        Returns:
            Parsed API response dict containing a list of ticker objects.
        """
        params = {"instType": inst_type}
        return self._http.get(c.TICKERS_INFO, params)

    def get_ticker(self, inst_id: str) -> dict:
        """Retrieve ticker data for a single instrument.

        Args:
            inst_id: Instrument ID, e.g. ``"BTC-JPY"``.

        Returns:
            Parsed API response dict containing the ticker object.
        """
        params = {"instId": inst_id}
        return self._http.get(c.TICKER_INFO, params)

    # ── Order Book ────────────────────────────────────────────────────────────

    def get_orderbook(self, inst_id: str, *, sz: str = "") -> dict:
        """Retrieve the order book (depth) for an instrument.

        Args:
            inst_id: Instrument ID.
            sz:      Number of depth levels to return (default 1, max 400).

        Returns:
            Parsed API response dict containing ``bids`` and ``asks`` arrays.
        """
        params = {"instId": inst_id, "sz": sz}
        return self._http.get(c.ORDER_BOOKS, params)

    def get_orderbook_full(self, inst_id: str, *, sz: str = "") -> dict:
        """Retrieve the full order book for an instrument (up to 5000 levels).

        Args:
            inst_id: Instrument ID.
            sz:      Number of depth levels to return.

        Returns:
            Parsed API response dict.
        """
        params = {"instId": inst_id, "sz": sz}
        return self._http.get(c.GET_BOOKS_FULL, params)

    # ── Candlesticks ──────────────────────────────────────────────────────────

    def get_candlesticks(
        self,
        inst_id: str,
        *,
        after: str = "",
        before: str = "",
        bar: str = "",
        limit: str = "",
    ) -> dict:
        """Retrieve candlestick (OHLCV) data.

        Args:
            inst_id: Instrument ID.
            bar:     Candle interval, e.g. ``"1m"``, ``"5m"``, ``"1H"``, ``"1D"``.
            after:   Pagination cursor — return data before this timestamp (ms).
            before:  Pagination cursor — return data after this timestamp (ms).
            limit:   Number of candles to return (max 300).

        Returns:
            Parsed API response dict.
        """
        params = {"instId": inst_id, "after": after, "before": before, "bar": bar, "limit": limit}
        return self._http.get(c.MARKET_CANDLES, params)

    def get_history_candlesticks(
        self,
        inst_id: str,
        *,
        after: str = "",
        before: str = "",
        bar: str = "",
        limit: str = "",
    ) -> dict:
        """Retrieve historical candlestick data (top-volume currencies only).

        Args:
            inst_id: Instrument ID.
            bar:     Candle interval.
            limit:   Number of candles to return (max 100).

        Returns:
            Parsed API response dict.
        """
        params = {"instId": inst_id, "after": after, "before": before, "bar": bar, "limit": limit}
        return self._http.get(c.HISTORY_CANDLES, params)

    # ── Trades ────────────────────────────────────────────────────────────────

    def get_trades(self, inst_id: str, *, limit: str = "") -> dict:
        """Retrieve the most recent trades for an instrument.

        Args:
            inst_id: Instrument ID.
            limit:   Number of trades to return (max 500).

        Returns:
            Parsed API response dict.
        """
        params = {"instId": inst_id, "limit": limit}
        return self._http.get(c.MARKET_TRADES, params)

    # ── Platform Volume ───────────────────────────────────────────────────────

    def get_volume(self) -> dict:
        """Retrieve the platform's 24-hour trading volume.

        Returns:
            Parsed API response dict containing volume in USD and BTC.
        """
        return self._http.get(c.VOLUME)

    # ── Call Auction ──────────────────────────────────────────────────────────

    def get_call_auction_details(self, inst_id: str) -> dict:
        """Retrieve call auction details for an instrument.

        Args:
            inst_id: Instrument ID.

        Returns:
            Parsed API response dict.
        """
        params = {"instId": inst_id}
        return self._http.get(c.GET_CALL_AUCTION_DETAILS, params)
