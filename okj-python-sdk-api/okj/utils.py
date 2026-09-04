"""Internal utilities for request signing and parameter serialisation.

These helpers are implementation details consumed by :mod:`okj._http`.
They are not part of the public SDK API.
"""

from __future__ import annotations

import base64
import datetime
import hmac
from urllib.parse import quote, urlencode


def get_timestamp() -> str:
    """Return the current UTC time formatted as an ISO-8601 string.

    Example: ``"2024-01-15T08:30:00.123Z"``
    """
    now = datetime.datetime.utcnow()
    return now.isoformat("T", "milliseconds") + "Z"


def sign(message: str, secret_key: str) -> bytes:
    """HMAC-SHA256 sign *message* with *secret_key* and return base64-encoded bytes.

    Args:
        message:    The pre-hash string to sign.
        secret_key: The API secret key.

    Returns:
        Base64-encoded signature bytes.
    """
    mac = hmac.new(
        bytes(secret_key, encoding="utf-8"),
        bytes(message, encoding="utf-8"),
        digestmod="sha256",
    )
    return base64.b64encode(mac.digest())


def build_pre_hash(timestamp: str, method: str, request_path: str, body: str) -> str:
    """Construct the pre-hash string used for HMAC signing.

    Format: ``<timestamp><METHOD><path><body>``

    Args:
        timestamp:    ISO-8601 UTC timestamp string.
        method:       HTTP method in uppercase (``"GET"`` or ``"POST"``).
        request_path: Full path including query string for GET requests.
        body:         JSON body string for POST requests, empty string for GET.

    Returns:
        The concatenated pre-hash string.
    """
    return timestamp + method.upper() + request_path + body


def build_query_string(params: dict) -> str:
    """Serialise *params* into a percent-encoded query string, skipping empty / None values.

    The encoding is not cosmetic. The string returned here is both appended to
    the URL *and* fed to :func:`build_pre_hash`, and ``httpx`` re-encodes
    whatever URL it is handed — a raw space leaves as ``%20``. Returning the
    space unencoded therefore signs one string and sends another, and the server
    answers with a generic auth error indistinguishable from a wrong key.
    ``quote`` is idempotent over already-encoded input, so httpx does not
    double-encode what this produces.

    ``safe=""`` leaves unreserved characters (alphanumerics and ``-._~``) alone,
    which is every parameter value this SDK sends today — so existing calls are
    byte-identical and their signatures unchanged.

    Args:
        params: Dict of query parameters.

    Returns:
        Query string starting with ``"?"`` if any params are present,
        otherwise an empty string.
    """
    kept = {k: v for k, v in params.items() if v is not None and v != ""}
    return ("?" + urlencode(kept, quote_via=quote)) if kept else ""


def build_signed_headers(
    api_key: str,
    secret_key: str,
    passphrase: str,
    timestamp: str,
    method: str,
    request_path: str,
    body: str,
    debug: bool = False,
) -> dict:
    """Build the full set of auth headers for a signed private request.

    Args:
        api_key:      API key string.
        secret_key:   API secret key string.
        passphrase:   API passphrase string.
        timestamp:    ISO-8601 UTC timestamp.
        method:       HTTP method (``"GET"`` or ``"POST"``).
        request_path: Request path including any query string.
        body:         JSON body string (empty for GET requests).
        debug:        If ``True``, log the pre-hash and resulting headers.

    Returns:
        Dict of HTTP headers ready to pass to the HTTP client.
    """
    from loguru import logger

    pre_hash = build_pre_hash(timestamp, method, request_path, body)
    if debug:
        logger.debug(f"[OKJ] pre_hash: {pre_hash}")

    signature = sign(pre_hash, secret_key)

    headers = {
        "Content-Type": "application/json",
        "OK-ACCESS-KEY": api_key,
        "OK-ACCESS-SIGN": signature,
        "OK-ACCESS-TIMESTAMP": timestamp,
        "OK-ACCESS-PASSPHRASE": passphrase,
        "X-BrokerID": "0",
    }
    if debug:
        masked = {
            **headers,
            "OK-ACCESS-KEY": api_key[:4] + "****",
            "OK-ACCESS-PASSPHRASE": "****",
        }
        logger.debug(f"[OKJ] headers: {masked}")

    return headers


def build_public_headers() -> dict:
    """Build minimal headers for an unsigned public endpoint request.

    Returns:
        Dict containing only the ``Content-Type`` header.
    """
    return {"Content-Type": "application/json"}
