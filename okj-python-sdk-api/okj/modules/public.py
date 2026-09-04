"""Public Data API — instruments and system time (no authentication required).

Accessed via ``client.public`` on an :class:`okj.OkjClient` instance.
"""

from __future__ import annotations

from .._http import _HttpClient
from .. import consts as c


class PublicAPI:
    """Provides access to the OKJ Public Data REST endpoints.

    These endpoints do not require API key authentication.

    Do not instantiate directly; use :class:`okj.OkjClient` instead::

        client = OkjClient()  # no credentials needed for public endpoints
        instruments = client.public.get_instruments(inst_type="SPOT")
    """

    def __init__(self, http: _HttpClient) -> None:
        self._http = http

    def get_instruments(
        self,
        inst_type: str,
        *,
        uly: str = "",
        inst_id: str = "",
    ) -> dict:
        """Retrieve the list of tradable instruments.

        Args:
            inst_type: Instrument type — ``"SPOT"``, ``"FUTURES"``, ``"OPTION"``, etc.
            uly:       Underlying asset filter (for derivatives).
            inst_id:   Instrument ID filter for a specific instrument.

        Returns:
            Parsed API response dict containing instrument specifications.
        """
        params = {"instType": inst_type, "uly": uly, "instId": inst_id}
        return self._http.get(c.INSTRUMENT_INFO, params)

    def get_system_time(self) -> dict:
        """Retrieve the current OKJ server time.

        Useful for synchronising client clocks before signing requests.

        Returns:
            Parsed API response dict containing ``ts`` in milliseconds.
        """
        return self._http.get(c.SYSTEM_TIME)
