"""Public Data API usage examples.

Demonstrates instrument listing and server time retrieval — both endpoints
require no API key authentication.

Run a specific example by uncommenting it in the ``if __name__ == "__main__"``
block at the bottom of this file, then execute:

    python test/public_test.py
"""

from okj import OkjClient
from api_config import DOMAIN


def get_client() -> OkjClient:
    # Public endpoints require no credentials.
    return OkjClient(base_url=DOMAIN)


def example_get_instruments_spot(client: OkjClient) -> dict:
    """Retrieve all available SPOT instruments."""
    return client.public.get_instruments(inst_type="SPOT")


def example_get_instruments_by_id(client: OkjClient) -> dict:
    """Retrieve instrument details for BTC-JPY specifically."""
    return client.public.get_instruments(inst_type="SPOT", inst_id="BTC-JPY")


def example_get_system_time(client: OkjClient) -> dict:
    """Retrieve the current OKJ server timestamp (milliseconds)."""
    return client.public.get_system_time()


if __name__ == "__main__":
    import json

    client = get_client()

    # Uncomment the example you want to run:

    # print(json.dumps(example_get_instruments_spot(client), indent=2, ensure_ascii=False))
    # print(json.dumps(example_get_instruments_by_id(client), indent=2, ensure_ascii=False))
    # print(json.dumps(example_get_system_time(client), indent=2, ensure_ascii=False))

    client.close()
