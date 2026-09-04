"""OKJ API module classes.

Each class wraps a specific domain of the OKJ REST API and is exposed as an
attribute of :class:`okj.OkjClient`.

Usage::

    from okj import OkjClient

    client = OkjClient(api_key="...", api_secret_key="...", passphrase="...")
    client.trade.place_order(...)
    client.account.get_account_balance()
    client.market.get_ticker(instId="BTC-JPY")
"""

from .account import AccountAPI
from .funding import FundingAPI
from .market import MarketAPI
from .public import PublicAPI
from .trade import TradeAPI

__all__ = [
    "AccountAPI",
    "FundingAPI",
    "MarketAPI",
    "PublicAPI",
    "TradeAPI",
]
