"""Custom exceptions raised by the OKJ SDK.

Hierarchy
---------
- :class:`OkjError`         — common base for all OKJ SDK errors
  - :class:`OkjAPIError`    — API returned an error response (4xx / 5xx)
  - :class:`OkjRequestError` — network / transport-level failure
  - :class:`OkjParamsError` — invalid arguments passed by the caller
"""

from __future__ import annotations

from typing import Any


class OkjError(Exception):
    """Base class for all OKJ SDK exceptions."""


class OkjAPIError(OkjError):
    """Raised when the OKJ REST API returns an error payload.

    Attributes:
        code:        API-level error code (``int`` or ``"unknown"``).
        message:     Human-readable error description from the API.
        status_code: HTTP status code of the response.
        response:    The raw :class:`httpx.Response` object.
        request:     The originating :class:`httpx.Request`, if available.
    """

    def __init__(self, response: Any) -> None:
        self.status_code: int = response.status_code
        self.response = response
        self.request = getattr(response, "request", None)
        self.code: int | str = 0
        self.message: str = ""

        try:
            body = response.json()
        except ValueError:
            self.message = f"Invalid JSON in OKJ API response: {response.text}"
            return

        if "code" in body and "msg" in body:
            self.code = body["code"]
            self.message = body["msg"]
        else:
            self.code = "unknown"
            self.message = "Unexpected API response format."

    def __str__(self) -> str:
        return (
            f"OkjAPIError(code={self.code}, http_status={self.status_code}): "
            f"{self.message}"
        )


class OkjRequestError(OkjError):
    """Raised when a network or transport-level error occurs.

    Attributes:
        message: Description of the transport failure.
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return f"OkjRequestError: {self.message}"


class OkjParamsError(OkjError):
    """Raised when the caller passes invalid or missing parameters.

    Attributes:
        message: Description of the parameter problem.
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return f"OkjParamsError: {self.message}"
