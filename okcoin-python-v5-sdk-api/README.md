### Overview
This is an unofficial Python wrapper for the [OKJ (OKCoin Japan) v5 API](https://dev.okj.com/apidoc/v5/en/)

If you came here looking to purchase cryptocurrencies from the OKJ exchange, please go [here](https://okj.com/).

Make sure you update often and check the [Changelog](https://dev.okj.com/apidoc/v5/log_en/) for new features and bug fixes.

### Features
- Implementation of all Rest API endpoints.
- Private and Public Websocket implementation
- Testnet support
- Websocket handling with reconnection and multiplexed connections

### Quick start
#### Prerequisites

`python version：>=3.9`

`WebSocketAPI： websockets package advise version 6.0`

#### Step 1: register an account on OKJ and apply for an API key
- Register for an account: https://www.okj.com/account/register
- Apply for an API key: https://www.okj.com/account/users/myApi

#### Step 2: install python-okj

```python
pip install python-okj
```

#### Step 3: Run examples

- Fill in API credentials in the corresponding examples
```python
api_key = ""
secret_key = ""
passphrase = ""
```
Runnable usage scripts live in `examples/`. Each one exposes `example_*`
functions and leaves every call commented out in its `__main__` block —
uncomment the one you want, then run it:

```bash
python examples/account_test.py
```

- Credentials and the target environment come from `examples/api_config.py`.
  **`DOMAIN` there defaults to production** (`https://api.okj.com`); switch it to
  the staging URL before running anything that places or cancels an order.
- RestAPI: `account_test.py`, `trade_test.py`, `market_test.py`,
  `funding_test.py`, `public_test.py`, `order_example.py`
- WebSocketAPI: `ws_private_test.py`, `ws_public_test.py`
- Pass `base_url=` to `OkjClient` to choose an environment; the URLs are listed
  in the [OKJ API documentation](https://dev.okj.com/apidoc/v5/en/)

#### Error handling

**A business error is a return value, not an exception.** Only HTTP >= 400
raises; a non-zero `code` on an HTTP 200 comes back as an ordinary dict. So
`try`/`except` alone is not enough — check `code` as well:

```python
from okj.exceptions import OkjAPIError, OkjRequestError

try:
    result = client.trade.get_order(inst_id="BTC-JPY", cl_ord_id="mine-1")
except OkjAPIError as exc:      # HTTP >= 400, e.g. 50113 Invalid Sign
    ...
except OkjRequestError as exc:  # network failure, or a 2xx that was not JSON
    ...
else:
    if result["code"] != "0":   # e.g. 51603 Order does not exist — HTTP 200
        ...
```

Both exception types derive from `OkjError`, so catching that alone is enough
if the distinction does not matter.

Note

- To learn more about OKJ API, visit official [OKJ API documentation](https://dev.okj.com/apidoc/v5/en/)

- If you face any questions when using `WebSocketAPI`,you can consult the following links

  - `asyncio`、`websockets` document/`github`：

    ```python
    https://docs.python.org/3/library/asyncio-dev.html
    https://websockets.readthedocs.io/en/stable/intro/index.html
    https://github.com/python-websockets/websockets
    ```

  - About `code=1006`：

    ```python
    https://github.com/Rapptz/discord.py/issues/1996
    https://github.com/python-websockets/websockets/issues/587
    ```
