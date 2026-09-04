"""Private WebSocket client — authenticated account and order channels.

Usage::

    import asyncio
    from okj.websocket import WsPrivateClient

    async def on_message(message: str) -> None:
        print("Received:", message)

    async def main():
        ws = WsPrivateClient(
            api_key="your_api_key",
            api_secret_key="your_api_secret_key",
            passphrase="your_passphrase",
            url="wss://ws.okj.com/ws/v5/private",
        )
        await ws.start()
        await ws.subscribe(
            args=[{"channel": "orders", "instType": "SPOT", "instId": "BTC-JPY"}],
            callback=on_message,
        )
        await asyncio.sleep(30)
        await ws.stop()

    asyncio.run(main())
"""

from __future__ import annotations

import asyncio
import json
from collections.abc import Callable

from loguru import logger

from .. import consts as c
from .ws_client import WsClient
from .ws_utils import build_login_payload


class WsPrivateClient:
    """Asynchronous WebSocket client for OKJ private (authenticated) channels.

    Authentication is performed automatically on :meth:`subscribe`.

    Parameters:
        api_key:         OKJ API key.
        api_secret_key:  OKJ API secret key.
        passphrase:      OKJ API passphrase.
        url:             Private WebSocket endpoint URL.
        base_url:        REST base URL used only when ``use_server_time`` is
                         ``True``, to read the server clock the login signature is
                         stamped with. Point it at the same environment as the
                         WebSocket URL: leaving it on production while connecting
                         to UAT stamps one environment's clock onto the other's
                         signature. Defaults to :data:`okj.consts.DEFAULT_BASE_URL`.
        use_server_time: When ``True``, use OKJ server time for auth signatures.
    """

    def __init__(
        self,
        api_key: str,
        api_secret_key: str,
        passphrase: str,
        url: str,
        *,
        use_server_time: bool = False,
        base_url: str = c.DEFAULT_BASE_URL,
    ) -> None:
        self._api_key = api_key
        self._api_secret_key = api_secret_key
        self._passphrase = passphrase
        self._use_server_time = use_server_time
        self._base_url = base_url
        self._callback: Callable[[str], None] | None = None
        self._ws_client = WsClient(url)
        self._websocket = None
        self._loop = asyncio.get_event_loop()

    async def start(self) -> None:
        """Connect to the WebSocket and begin consuming messages in the background."""
        logger.info("Connecting to private WebSocket: %s", self._ws_client.url)
        self._websocket = await self._ws_client.connect()
        self._loop.create_task(self._consume())

    async def subscribe(self, args: list[dict], callback: Callable[[str], None]) -> None:
        """Authenticate and subscribe to one or more private channels.

        Login is performed automatically before sending the subscription.

        Args:
            args:     Channel subscription dicts, e.g.
                      ``[{"channel": "orders", "instType": "SPOT"}]``.
            callback: Callable invoked with each received message string.
        """
        self._callback = callback
        await self._login()
        # Allow time for the login acknowledgement before subscribing.
        await asyncio.sleep(5)
        payload = json.dumps({"op": "subscribe", "args": args})
        await self._websocket.send(payload)
        logger.info("Subscribed to private channels: %s", args)

    async def unsubscribe(self, args: list[dict], callback: Callable[[str], None]) -> None:
        """Unsubscribe from one or more private channels.

        Args:
            args:     Channel subscription dicts to unsubscribe from.
            callback: Callback for acknowledgement messages.
        """
        self._callback = callback
        payload = json.dumps({"op": "unsubscribe", "args": args})
        logger.info("Unsubscribing from private channels: %s", args)
        await self._websocket.send(payload)

    async def send_order(self, payload: list | dict, callback: Callable[[str], None]) -> None:
        """Send a WebSocket trade order message.

        Args:
            payload:  Order payload dict or list of dicts.
            callback: Callback for the order response.
        """
        self._callback = callback
        await self._websocket.send(json.dumps(payload))

    async def stop(self) -> None:
        """Close the connection and stop the event loop."""
        await self._ws_client.close()
        self._loop.stop()

    # ── Internal ──────────────────────────────────────────────────────────────

    async def _login(self) -> None:
        """Send the authentication login message."""
        login_payload = build_login_payload(
            api_key=self._api_key,
            passphrase=self._passphrase,
            secret_key=self._api_secret_key,
            use_server_time=self._use_server_time,
            base_url=self._base_url,
        )
        await self._websocket.send(login_payload)
        logger.info("Login message sent.")

    async def _consume(self) -> None:
        """Continuously read messages and dispatch them to the registered callback."""
        async for message in self._websocket:
            logger.debug("Private WS message: %s", message)
            if self._callback is not None:
                self._callback(message)
