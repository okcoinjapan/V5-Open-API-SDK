"""Internal HTTP client — not part of the public SDK API.

:class:`_HttpClient` is a thin wrapper around :class:`httpx.Client` that
handles request signing, header construction, and JSON deserialisation.
API module classes (TradeAPI, AccountAPI, …) hold a reference to this client
rather than inheriting from it, keeping the transport concern isolated.
"""

from __future__ import annotations

import json
from typing import Any, Optional

import httpx
from loguru import logger

from . import consts as c
from . import utils
from .exceptions import OkjAPIError, OkjRequestError


class _HttpClient:
    """Authenticated REST client shared across all API module instances.

    Parameters:
        api_key:        OKJ API key.  Pass an empty string for public endpoints.
        api_secret_key: OKJ API secret key.
        passphrase:     OKJ API passphrase.
        base_url:       Base URL of the OKJ REST API.
        debug:          When ``True``, log request details via *loguru*.
        proxy:          Optional HTTP/HTTPS proxy URL passed to *httpx*.
    """

    def __init__(
        self,
        api_key: str,
        api_secret_key: str,
        passphrase: str,
        base_url: str,
        debug: bool,
        proxy: Optional[str],
    ) -> None:
        self._api_key = api_key
        self._api_secret_key = api_secret_key
        self._passphrase = passphrase
        self._base_url = base_url.rstrip("/")
        self._debug = debug
        self._session = httpx.Client(
            base_url=self._base_url,
            http2=True,
            proxy=proxy,
            follow_redirects=True,
            timeout=httpx.Timeout(connect=10.0, read=30.0, write=10.0, pool=5.0),
        )

    # ── Public interface used by API module classes ────────────────────────────

    def get(self, path: str, params: Optional[dict] = None) -> dict:
        """Send a signed GET request.

        Args:
            path:   API endpoint path (e.g. ``"/api/v5/trade/order"``).
            params: Optional query parameters dict.

        Returns:
            Parsed JSON response body as a dict.
        """
        return self._request(c.GET, path, params or {})

    def post(self, path: str, body: Optional[dict | list] = None) -> dict:
        """Send a signed POST request.

        Args:
            path: API endpoint path.
            body: Optional request body — either a dict or a list of dicts
                  (used for batch endpoints).

        Returns:
            Parsed JSON response body as a dict.
        """
        return self._request(c.POST, path, body or {})

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _request(self, method: str, path: str, params: dict | list) -> dict:
        """Build, sign, send a request and return its parsed JSON response."""
        timestamp = utils.get_timestamp()

        if method == c.GET:
            # For GET requests, append params as query string; body is empty.
            full_path = path + utils.build_query_string(params)  # type: ignore[arg-type]
            body_str = ""
        else:
            full_path = path
            # Strip empty / None values from POST body to keep payloads clean.
            if isinstance(params, list):
                body_str = json.dumps(params)
            else:
                body_str = json.dumps(
                    {k: v for k, v in params.items() if v is not None and v != ""}
                )

        if self._debug:
            logger.debug(f"[OKJ] {method} {self._base_url}{full_path}")
            if body_str:
                logger.debug(f"[OKJ] body: {body_str}")

        # Choose signed vs. unsigned headers based on whether an API key is set.
        if self._api_key:
            headers = utils.build_signed_headers(
                api_key=self._api_key,
                secret_key=self._api_secret_key,
                passphrase=self._passphrase,
                timestamp=timestamp,
                method=method,
                request_path=full_path,
                body=body_str,
                debug=self._debug,
            )
        else:
            headers = utils.build_public_headers()

        try:
            if method == c.GET:
                response = self._session.get(full_path, headers=headers)
            else:
                response = self._session.post(full_path, content=body_str, headers=headers)
        except httpx.RequestError as exc:
            raise OkjRequestError(str(exc)) from exc

        if self._debug:
            logger.debug(f"[OKJ] HTTP {response.status_code}")

        # Raise for non-2xx responses that carry an API error payload.
        if response.status_code >= 400:
            raise OkjAPIError(response)

        try:
            return response.json()
        except Exception as exc:
            raise OkjRequestError(
                f"Failed to parse response as JSON (HTTP {response.status_code}): {response.text[:200]}"
            ) from exc

    # ── Resource management ───────────────────────────────────────────────────

    def close(self) -> None:
        """Close the underlying HTTP session and release connections."""
        self._session.close()

    def __enter__(self) -> "_HttpClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
