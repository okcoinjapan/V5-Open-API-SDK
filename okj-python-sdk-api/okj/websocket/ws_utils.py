"""WebSocket utility functions — login payload construction and helpers.

Internal module; not part of the public SDK API.
"""

from __future__ import annotations

import base64
import hmac
import json
import time

from loguru import logger

from .. import consts as c


def build_login_payload(
    api_key: str,
    passphrase: str,
    secret_key: str,
    *,
    use_server_time: bool = False,
    base_url: str = c.DEFAULT_BASE_URL,
) -> str:
    """Build the JSON login payload for WebSocket authentication.

    Args:
        api_key:         OKJ API key.
        passphrase:      OKJ API passphrase.
        secret_key:      OKJ API secret key.
        use_server_time: When ``True``, fetch the timestamp from the OKJ server
                         instead of using local time.  Defaults to ``False``.
        base_url:        REST base URL the server time is read from.  Must be the
                         same host the caller's :class:`~okj.client.OkjClient`
                         uses, or the signature is stamped with one environment's
                         clock and presented to another.  Defaults to
                         :data:`okj.consts.DEFAULT_BASE_URL`.

    Returns:
        JSON-encoded login payload string ready to send over the WebSocket.
    """
    timestamp = _get_server_time(base_url) if use_server_time else _get_local_time()
    message = f"{timestamp}GET/users/self/verify"

    mac = hmac.new(
        bytes(secret_key, encoding="utf-8"),
        bytes(message, encoding="utf-8"),
        digestmod="sha256",
    )
    signature = base64.b64encode(mac.digest()).decode("utf-8")

    payload = {
        "op": "login",
        "args": [{
            "apiKey": api_key,
            "passphrase": passphrase,
            "timestamp": timestamp,
            "sign": signature,
        }],
    }
    return json.dumps(payload)


def _get_local_time() -> int:
    """Return the current Unix timestamp in seconds."""
    return int(time.time())


def _get_server_time(base_url: str = c.DEFAULT_BASE_URL) -> str:
    """Fetch the current timestamp from the OKJ public time endpoint.

    Falls back to local time if the request fails.

    Args:
        base_url: REST base URL to read the server time from.

    Returns:
        Timestamp string in milliseconds, or local Unix timestamp on failure.

    Note:
        The URL is composed from :data:`okj.consts.DEFAULT_BASE_URL` and
        :data:`okj.consts.SYSTEM_TIME` rather than written out here. Both already
        existed; spelling the endpoint a second time meant one path in two places,
        and changing one of them would have left the other pointing elsewhere.

        The fallback is deliberate but no longer silent. A login signature carries
        a timestamp, and the server rejects one that is too far from its own clock
        — so a machine with a skewed clock fails authentication with an error that
        says nothing about where the time came from. Whoever debugs that needs to
        see that this request failed.
    """
    import httpx

    url = f"{base_url}{c.SYSTEM_TIME}"
    try:
        response = httpx.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()["data"][0]["ts"]
        logger.warning(
            "Server time request to {} returned {}; falling back to local time, "
            "which will fail authentication if this clock is skewed",
            url,
            response.status_code,
        )
    except Exception as failure:
        logger.warning(
            "Server time request to {} failed ({}); falling back to local time, "
            "which will fail authentication if this clock is skewed",
            url,
            failure,
        )

    return str(_get_local_time())
