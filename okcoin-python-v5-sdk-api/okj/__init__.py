"""python-okj — Python SDK for the OKJ (OKCoin Japan) API v5.

The primary entry point is :class:`OkjClient`.  All REST API domains are
accessible as attributes of that class.

Typical usage::

    from okj import OkjClient

    client = OkjClient(
        api_key="your_api_key",
        api_secret_key="your_api_secret_key",
        passphrase="your_passphrase",
    )

    ticker = client.market.get_ticker(inst_id="BTC-JPY")
    balance = client.account.get_account_balance()

WebSocket usage::

    from okj.websocket import WsPublicClient, WsPrivateClient

Exception hierarchy::

    OkjError
    ├── OkjAPIError      — API returned a 4xx / 5xx response
    ├── OkjRequestError  — network / transport-level failure
    └── OkjParamsError   — invalid arguments passed by the caller
"""

from .client import OkjClient
from .exceptions import OkjAPIError, OkjError, OkjParamsError, OkjRequestError

__version__ = "1.1.0"
__all__ = ["OkjClient", "OkjError", "OkjAPIError", "OkjRequestError", "OkjParamsError"]
