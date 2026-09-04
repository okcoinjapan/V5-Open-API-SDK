"""Public WebSocket client — subscribe to market data channels.

Usage::

    import asyncio
    from okj.websocket import WsPublicClient

    async def on_message(message: str) -> None:
        print("Received:", message)

    async def main():
        ws = WsPublicClient(url="wss://ws.okj.com/ws/v5/public")
        await ws.start()
        await ws.subscribe(
            args=[{"channel": "tickers", "instId": "BTC-JPY"}],
            callback=on_message,
        )
        await asyncio.sleep(30)
        await ws.stop()

    asyncio.run(main())
"""

from __future__ import annotations

import asyncio
import json
from typing import Callable

from loguru import logger

from .ws_client import WsClient


class WsPublicClient:
    """Asynchronous WebSocket client for OKJ public market data channels.

    Parameters:
        url: Public WebSocket endpoint URL.
    """

    def __init__(self, url: str) -> None:
        self.url = url
        self._callback: Callable[[str], None] | None = None
        self._ws_client = WsClient(url)
        self._websocket = None
        self._loop = asyncio.get_event_loop()

    async def start(self) -> None:
        """Connect to the WebSocket and begin consuming messages in the background."""
        logger.info("Connecting to public WebSocket: %s", self.url)
        self._websocket = await self._ws_client.connect()
        self._loop.create_task(self._consume())

    async def subscribe(self, args: list[dict], callback: Callable[[str], None]) -> None:
        """Subscribe to one or more public channels.

        Args:
            args:     List of channel subscription dicts, e.g.
                      ``[{"channel": "tickers", "instId": "BTC-JPY"}]``.
            callback: Coroutine or callable invoked with each received message string.
        """
        self._callback = callback
        payload = json.dumps({"op": "subscribe", "args": args})
        await self._websocket.send(payload)
        logger.info("Subscribed to: %s", args)

    async def unsubscribe(self, args: list[dict], callback: Callable[[str], None]) -> None:
        """Unsubscribe from one or more public channels.

        Args:
            args:     Channel subscription dicts to unsubscribe from.
            callback: Callback to invoke for any acknowledgement messages.
        """
        self._callback = callback
        payload = json.dumps({"op": "unsubscribe", "args": args})
        logger.info("Unsubscribing from: %s", args)
        await self._websocket.send(payload)

    async def stop(self) -> None:
        """Unsubscribe, close the connection, and stop the event loop."""
        await self._ws_client.close()
        self._loop.stop()

    # ── Internal ──────────────────────────────────────────────────────────────

    async def _consume(self) -> None:
        """Continuously read messages and dispatch them to the registered callback."""
        async for message in self._websocket:
            logger.debug("Public WS message: %s", message)
            if self._callback is not None:
                self._callback(message)
