"""Private WebSocket usage example.

Demonstrates subscribing to authenticated private channels such as account
balance updates and live order notifications.

Run this example with:

    python test/ws_private_test.py
"""

import asyncio

from okj.websocket import WsPrivateClient
from api_config import API_KEY, API_SECRET_KEY, PASSPHRASE, PRIVATE_URL


def on_message(message: str) -> None:
    """Handle incoming WebSocket messages."""
    print("Message received:", message)


async def main() -> None:
    ws = WsPrivateClient(
        api_key=API_KEY,
        api_secret_key=API_SECRET_KEY,
        passphrase=PASSPHRASE,
        url=PRIVATE_URL,
    )
    await ws.start()

    # Subscribe to account balance updates and BTC-JPY order notifications.
    # Authentication (login) is handled automatically before subscribing.
    await ws.subscribe(
        args=[
            {"channel": "account", "ccy": "JPY"},
            {"channel": "orders", "instType": "SPOT", "instId": "BTC-JPY"},
        ],
        callback=on_message,
    )

    # Receive messages for 30 seconds.
    await asyncio.sleep(30)

    print("Unsubscribing...")
    await ws.unsubscribe(
        args=[{"channel": "orders", "instType": "SPOT", "instId": "BTC-JPY"}],
        callback=on_message,
    )

    await asyncio.sleep(5)
    await ws.stop()


if __name__ == "__main__":
    asyncio.run(main())
