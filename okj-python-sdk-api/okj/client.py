"""OKJ SDK unified client entry point.

:class:`OkjClient` is the single object users need to import.  It exposes all
REST API domains as attributes and manages the shared HTTP session.

Quick start::

    from okj import OkjClient

    client = OkjClient(
        api_key="your_api_key",
        api_secret_key="your_api_secret_key",
        passphrase="your_passphrase",
        base_url="https://api.okj.com",
    )

    # Market data (no auth needed)
    ticker = client.market.get_ticker(instId="BTC-JPY")

    # Place a limit buy order
    result = client.trade.place_order(
        instId="BTC-JPY",
        tdMode="cash",
        side="buy",
        ordType="limit",
        sz="0.001",
        px="5000000",
    )

    # Always close the session when done (or use as a context manager)
    client.close()

Context manager usage::

    with OkjClient(api_key="...", api_secret_key="...", passphrase="...") as client:
        balance = client.account.get_account_balance()
"""

from __future__ import annotations

from typing import Any, Optional

from . import consts as c
from ._http import _HttpClient
from .modules.account import AccountAPI
from .modules.funding import FundingAPI
from .modules.market import MarketAPI
from .modules.public import PublicAPI
from .modules.trade import TradeAPI


class OkjClient:
    """Unified OKJ API client.

    All REST API domains are exposed as attributes:

    - :attr:`trade`   — :class:`~okj.modules.trade.TradeAPI`
    - :attr:`account` — :class:`~okj.modules.account.AccountAPI`
    - :attr:`market`  — :class:`~okj.modules.market.MarketAPI`
    - :attr:`funding` — :class:`~okj.modules.funding.FundingAPI`
    - :attr:`public`  — :class:`~okj.modules.public.PublicAPI`

    Parameters:
        api_key:        OKJ API key.  Leave empty for public-only access.
        api_secret_key: OKJ API secret key.
        passphrase:     OKJ API passphrase.
        base_url:       Base URL of the REST API.  Defaults to
                        ``"https://api.okj.com"``.
        debug:          When ``True``, log request details (URL, headers, body)
                        via *loguru*.  Defaults to ``False``.
        proxy:          Optional HTTP/HTTPS proxy URL forwarded to *httpx*.
    """

    def __init__(
        self,
        api_key: str = "",
        api_secret_key: str = "",
        passphrase: str = "",
        base_url: str = c.DEFAULT_BASE_URL,
        debug: bool = False,
        proxy: Optional[str] = None,
    ) -> None:
        # Shared HTTP client — all modules send requests through this instance.
        self._http = _HttpClient(
            api_key=api_key,
            api_secret_key=api_secret_key,
            passphrase=passphrase,
            base_url=base_url,
            debug=debug,
            proxy=proxy,
        )

        # REST API domain modules
        self.trade = TradeAPI(self._http)
        self.account = AccountAPI(self._http)
        self.market = MarketAPI(self._http)
        self.funding = FundingAPI(self._http)
        self.public = PublicAPI(self._http)

    def close(self) -> None:
        """Close the underlying HTTP session and release connections.

        Call this when finished to avoid resource leaks, or use the client
        as a context manager (``with OkjClient(...) as client: ...``).
        """
        self._http.close()

    def __enter__(self) -> "OkjClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def __repr__(self) -> str:
        masked_key = self._http._api_key[:8] + "..." if self._http._api_key else "(public)"
        return f"OkjClient(api_key={masked_key!r}, base_url={self._http._base_url!r})"
