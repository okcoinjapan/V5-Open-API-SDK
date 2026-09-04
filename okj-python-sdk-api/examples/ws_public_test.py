"""Public WebSocket usage example.

Demonstrates subscribing to public market data channels such as tickers,
order books, and trades — no authentication required.

Run this example with:

    python test/ws_public_test.py
"""

import asyncio

from okj.websocket import WsPublicClient
from api_config import PUBLIC_URL


def on_message(message: str) -> None:
    """Handle incoming WebSocket messages."""
    print("Message received:", message)


async def main() -> None:
    ws = WsPublicClient(url=PUBLIC_URL)
    await ws.start()

    # Subscribe to BTC-JPY ticker and order book channels.
    await ws.subscribe(
        args=[
            {"channel": "tickers", "instId": "BTC-JPY"},
            {"channel": "books", "instId": "BTC-JPY"},
        ],
        callback=on_message,
    )

    # Receive messages for 30 seconds.
    await asyncio.sleep(30)

    print("Unsubscribing...")
    await ws.unsubscribe(
        args=[{"channel": "tickers", "instId": "BTC-JPY"}],
        callback=on_message,
    )

    await asyncio.sleep(5)
    await ws.stop()


if __name__ == "__main__":
    asyncio.run(main())
