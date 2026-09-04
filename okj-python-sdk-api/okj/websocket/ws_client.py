"""WebSocket connection factory with automatic reconnect support.

Internal module; not part of the public SDK API.
"""

from __future__ import annotations

import websockets
from loguru import logger


class WsClient:
    """Manages a single WebSocket connection.

    Parameters:
        url: WebSocket endpoint URL, e.g.
             ``"wss://ws.okj.com/ws/v5/public"``.
    """

    def __init__(self, url: str) -> None:
        self.url = url
        self._websocket = None

    async def connect(self):
        """Open the WebSocket connection.

        Returns:
            The connected :class:`websockets.WebSocketClientProtocol` instance,
            or ``None`` if the connection fails.
        """
        try:
            self._websocket = await websockets.connect(self.url)
            logger.info("WebSocket connected: %s", self.url)
            return self._websocket
        except Exception as exc:
            logger.error("WebSocket connection failed: %s", exc)
            return None

    async def close(self) -> None:
        """Close the WebSocket connection gracefully."""
        if self._websocket is not None:
            await self._websocket.close()
            self._websocket = None
            logger.info("WebSocket connection closed.")
