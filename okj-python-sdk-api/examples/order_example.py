"""Order placement and retrieval example.

Places a limit buy order at the current market price and then queries it.

Run this example with:

    python test/order_example.py
"""

import json
import time

from okj import OkjClient
from api_config import API_KEY, API_SECRET_KEY, PASSPHRASE, DOMAIN

INST_ID = "APT-JPY"


def main() -> None:
    client = OkjClient(
        api_key=API_KEY,
        api_secret_key=API_SECRET_KEY,
        passphrase=PASSPHRASE,
        base_url=DOMAIN,
    )

    # Fetch the current market price.
    ticker = client.market.get_ticker(inst_id=INST_ID)
    last_px = ticker["data"][0]["last"]
    print(f"Current {INST_ID} price: {last_px}")

    # Place a limit buy order at the current price (quantity: 1).
    print("\n=== Place order ===")
    place_result = client.trade.place_order(
        inst_id=INST_ID,
        td_mode="cash",
        side="buy",
        ord_type="limit",
        sz="1",
        px=last_px,
    )
    print(json.dumps(place_result, indent=2, ensure_ascii=False))

    ord_id = ""
    if isinstance(place_result, dict) and place_result.get("data"):
        ord_id = place_result["data"][0].get("ordId", "")

    print(f"\nordId: {ord_id}")

    if ord_id:
        time.sleep(1)
        print("\n=== Get order ===")
        order_result = client.trade.get_order(inst_id=INST_ID, ord_id=ord_id)
        print(json.dumps(order_result, indent=2, ensure_ascii=False))
    else:
        print("Order placement failed — cannot query order.")

    client.close()


if __name__ == "__main__":
    main()
