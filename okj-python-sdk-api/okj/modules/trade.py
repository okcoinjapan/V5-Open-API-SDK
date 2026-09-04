"""Trade API — order placement, cancellation, amendment, and history.

Accessed via ``client.trade`` on an :class:`okj.OkjClient` instance.
"""

from __future__ import annotations

from typing import Any, Optional

from .._http import _HttpClient
from .. import consts as c


class TradeAPI:
    """Provides access to the OKJ Trade REST endpoints.

    Do not instantiate directly; use :class:`okj.OkjClient` instead::

        client = OkjClient(api_key="...", api_secret_key="...", passphrase="...")
        result = client.trade.place_order(
            inst_id="BTC-JPY", td_mode="cash", side="buy",
            ord_type="limit", sz="0.001", px="5000000",
        )
    """

    def __init__(self, http: _HttpClient) -> None:
        self._http = http

    # ── Standard orders ───────────────────────────────────────────────────────

    def place_order(
        self,
        inst_id: str,
        td_mode: str,
        side: str,
        ord_type: str,
        sz: str,
        *,
        ccy: str = "",
        cl_ord_id: str = "",
        tag: str = "",
        pos_side: str = "",
        px: str = "",
        tgt_ccy: str = "",
        tp_trigger_px: str = "",
        tp_ord_px: str = "",
        sl_trigger_px: str = "",
        sl_ord_px: str = "",
        tp_trigger_px_type: str = "",
        sl_trigger_px_type: str = "",
        stp_id: str = "",
        stp_mode: str = "",
        ban_amend: str = "",
        attach_algo_ords: Optional[list] = None,
    ) -> dict:
        """Place a new order.

        Args:
            inst_id:   Instrument ID, e.g. ``"BTC-JPY"``.
            td_mode:   Trade mode — ``"cash"`` for spot trading.
            side:      Order side — ``"buy"`` or ``"sell"``.
            ord_type:  Order type — ``"market"``, ``"limit"``, ``"post_only"``, etc.
            sz:        Order size (quantity).
            px:        Order price; required for limit orders.
            cl_ord_id: Client-assigned order ID (up to 32 characters).
            attach_algo_ords: Attached TP/SL algo orders (optional list of dicts).

        Returns:
            Parsed API response dict containing ``code``, ``msg``, and ``data``.
        """
        params: dict[str, Any] = {
            "instId": inst_id, "tdMode": td_mode, "side": side,
            "ordType": ord_type, "sz": sz, "ccy": ccy,
            "clOrdId": cl_ord_id, "tag": tag, "posSide": pos_side,
            "px": px, "tgtCcy": tgt_ccy,
            "tpTriggerPx": tp_trigger_px, "tpOrdPx": tp_ord_px,
            "slTriggerPx": sl_trigger_px, "slOrdPx": sl_ord_px,
            "tpTriggerPxType": tp_trigger_px_type, "slTriggerPxType": sl_trigger_px_type,
            "stpId": stp_id, "stpMode": stp_mode, "banAmend": ban_amend,
        }
        if attach_algo_ords is not None:
            params["attachAlgoOrds"] = attach_algo_ords
        return self._http.post(c.PLACE_ORDER, params)

    def place_multiple_orders(self, orders: list[dict]) -> dict:
        """Place multiple orders in a single request (batch).

        Args:
            orders: List of order parameter dicts (same fields as
                    :meth:`place_order`, but using camelCase API keys directly).

        Returns:
            Parsed API response dict.
        """
        return self._http.post(c.BATCH_ORDERS, orders)

    def cancel_order(
        self,
        inst_id: str,
        *,
        ord_id: str = "",
        cl_ord_id: str = "",
    ) -> dict:
        """Cancel a single open order.

        Provide either *ord_id* or *cl_ord_id*.

        Args:
            inst_id:   Instrument ID.
            ord_id:    Exchange-assigned order ID.
            cl_ord_id: Client-assigned order ID.

        Returns:
            Parsed API response dict.
        """
        params = {"instId": inst_id, "ordId": ord_id, "clOrdId": cl_ord_id}
        return self._http.post(c.CANCEL_ORDER, params)

    def cancel_multiple_orders(self, orders: list[dict]) -> dict:
        """Cancel multiple open orders in a single request.

        Args:
            orders: List of dicts, each containing ``instId`` and either
                    ``ordId`` or ``clOrdId``.

        Returns:
            Parsed API response dict.
        """
        return self._http.post(c.CANCEL_BATCH_ORDERS, orders)

    def amend_order(
        self,
        inst_id: str,
        *,
        cxl_on_fail: str = "",
        ord_id: str = "",
        cl_ord_id: str = "",
        req_id: str = "",
        new_sz: str = "",
        new_px: str = "",
        new_tp_trigger_px: str = "",
        new_tp_ord_px: str = "",
        new_sl_trigger_px: str = "",
        new_sl_ord_px: str = "",
        new_tp_trigger_px_type: str = "",
        new_sl_trigger_px_type: str = "",
        attach_algo_ords: Optional[list] = None,
    ) -> dict:
        """Amend an existing open order.

        Args:
            inst_id:  Instrument ID.
            ord_id:   Order ID to amend (provide *ord_id* or *cl_ord_id*).
            new_sz:   New order size.
            new_px:   New order price.

        Returns:
            Parsed API response dict.
        """
        params: dict[str, Any] = {
            "instId": inst_id, "cxlOnFail": cxl_on_fail,
            "ordId": ord_id, "clOrdId": cl_ord_id, "reqId": req_id,
            "newSz": new_sz, "newPx": new_px,
            "newTpTriggerPx": new_tp_trigger_px, "newTpOrdPx": new_tp_ord_px,
            "newSlTriggerPx": new_sl_trigger_px, "newSlOrdPx": new_sl_ord_px,
            "newTpTriggerPxType": new_tp_trigger_px_type,
            "newSlTriggerPxType": new_sl_trigger_px_type,
        }
        if attach_algo_ords is not None:
            params["attachAlgoOrds"] = attach_algo_ords
        return self._http.post(c.AMEND_ORDER, params)

    def amend_multiple_orders(self, orders: list[dict]) -> dict:
        """Amend multiple open orders in a single request.

        Args:
            orders: List of amendment parameter dicts.

        Returns:
            Parsed API response dict.
        """
        return self._http.post(c.AMEND_BATCH_ORDER, orders)

    def close_positions(
        self,
        inst_id: str,
        mgn_mode: str,
        *,
        pos_side: str = "",
        ccy: str = "",
        auto_cxl: str = "",
        cl_ord_id: str = "",
        tag: str = "",
    ) -> dict:
        """Close all open positions for an instrument.

        Args:
            inst_id:  Instrument ID.
            mgn_mode: Margin mode — ``"cross"`` or ``"isolated"``.
            pos_side: Position side — ``"long"``, ``"short"``, or ``"net"``.

        Returns:
            Parsed API response dict.
        """
        params = {
            "instId": inst_id, "mgnMode": mgn_mode, "posSide": pos_side,
            "ccy": ccy, "autoCxl": auto_cxl, "clOrdId": cl_ord_id, "tag": tag,
        }
        return self._http.post(c.CLOSE_POSITION, params)

    # ── Order queries ─────────────────────────────────────────────────────────

    def get_order(
        self,
        inst_id: str,
        *,
        ord_id: str = "",
        cl_ord_id: str = "",
    ) -> dict:
        """Retrieve details of a single order.

        Args:
            inst_id:   Instrument ID.
            ord_id:    Exchange order ID.
            cl_ord_id: Client order ID.

        Returns:
            Parsed API response dict.
        """
        params = {"instId": inst_id, "ordId": ord_id, "clOrdId": cl_ord_id}
        return self._http.get(c.ORDER_INFO, params)

    def get_order_list(
        self,
        *,
        inst_type: str = "",
        uly: str = "",
        inst_id: str = "",
        ord_type: str = "",
        state: str = "",
        after: str = "",
        before: str = "",
        limit: str = "",
    ) -> dict:
        """Retrieve the list of pending (unfilled) orders.

        Returns:
            Parsed API response dict.
        """
        params = {
            "instType": inst_type, "uly": uly, "instId": inst_id,
            "ordType": ord_type, "state": state,
            "after": after, "before": before, "limit": limit,
        }
        return self._http.get(c.ORDERS_PENDING, params)

    def get_orders_history(
        self,
        inst_type: str,
        *,
        uly: str = "",
        inst_id: str = "",
        ord_type: str = "",
        state: str = "",
        after: str = "",
        before: str = "",
        begin: str = "",
        end: str = "",
        limit: str = "",
    ) -> dict:
        """Retrieve order history from the last 7 days.

        Args:
            inst_type: Instrument type — ``"SPOT"``, ``"FUTURES"``, etc.

        Returns:
            Parsed API response dict.
        """
        params = {
            "instType": inst_type, "uly": uly, "instId": inst_id,
            "ordType": ord_type, "state": state,
            "after": after, "before": before,
            "begin": begin, "end": end, "limit": limit,
        }
        return self._http.get(c.ORDERS_HISTORY, params)

    def get_orders_history_archive(
        self,
        inst_type: str,
        *,
        uly: str = "",
        inst_id: str = "",
        ord_type: str = "",
        state: str = "",
        after: str = "",
        before: str = "",
        begin: str = "",
        end: str = "",
        limit: str = "",
    ) -> dict:
        """Retrieve order history from the last 3 months.

        Args:
            inst_type: Instrument type — ``"SPOT"``, ``"FUTURES"``, etc.

        Returns:
            Parsed API response dict.
        """
        params = {
            "instType": inst_type, "uly": uly, "instId": inst_id,
            "ordType": ord_type, "state": state,
            "after": after, "before": before,
            "begin": begin, "end": end, "limit": limit,
        }
        return self._http.get(c.ORDERS_HISTORY_ARCHIVE, params)

    def get_fills(
        self,
        *,
        inst_type: str = "",
        uly: str = "",
        inst_id: str = "",
        ord_id: str = "",
        after: str = "",
        before: str = "",
        limit: str = "",
        begin: str = "",
        end: str = "",
        sub_type: str = "",
    ) -> dict:
        """Retrieve transaction (fill) details from the last 3 days.

        Returns:
            Parsed API response dict.
        """
        params = {
            "instType": inst_type, "uly": uly, "instId": inst_id, "ordId": ord_id,
            "after": after, "before": before, "limit": limit,
            "begin": begin, "end": end, "subType": sub_type,
        }
        return self._http.get(c.ORDER_FILLS, params)

    def get_fills_history(
        self,
        inst_type: str,
        *,
        uly: str = "",
        inst_id: str = "",
        ord_id: str = "",
        after: str = "",
        before: str = "",
        limit: str = "",
        begin: str = "",
        end: str = "",
    ) -> dict:
        """Retrieve transaction (fill) details from the last 30 days.

        Args:
            inst_type: Instrument type — ``"SPOT"``, ``"FUTURES"``, etc.

        Returns:
            Parsed API response dict.
        """
        params = {
            "instType": inst_type, "uly": uly, "instId": inst_id, "ordId": ord_id,
            "after": after, "before": before, "limit": limit,
            "begin": begin, "end": end,
        }
        return self._http.get(c.ORDERS_FILLS_HISTORY, params)

    def cancel_all_orders(self, time_out: str, *, tag: str = "") -> dict:
        """Schedule cancellation of all open orders after *time_out* seconds.

        Args:
            time_out: Countdown in seconds (range 10–120).
            tag:      Optional order tag to filter which orders are cancelled.

        Returns:
            Parsed API response dict.
        """
        params = {"timeOut": time_out, "tag": tag}
        return self._http.post(c.CANCEL_ALL_ORDERS, params)

    # ── Algo orders ───────────────────────────────────────────────────────────

    def place_algo_order(
        self,
        *,
        inst_id: str = "",
        td_mode: str = "",
        side: str = "",
        ord_type: str = "",
        sz: str = "",
        tag: str = "",
        tgt_ccy: str = "",
        algo_cl_ord_id: str = "",
        tp_trigger_px: str = "",
        tp_trigger_px_type: str = "",
        tp_ord_px: str = "",
        sl_trigger_px: str = "",
        sl_trigger_px_type: str = "",
        sl_ord_px: str = "",
    ) -> dict:
        """Place an algo (conditional / TP-SL) order.

        Args:
            inst_id:  Instrument ID.
            ord_type: Algo type — ``"conditional"``, ``"oco"``, ``"trigger"``, etc.
            side:     ``"buy"`` or ``"sell"``.
            sz:       Order size.

        Returns:
            Parsed API response dict.
        """
        params = {
            "instId": inst_id, "tdMode": td_mode, "side": side, "ordType": ord_type,
            "sz": sz, "tag": tag, "tgtCcy": tgt_ccy, "algoClOrdId": algo_cl_ord_id,
            "tpTriggerPx": tp_trigger_px, "tpTriggerPxType": tp_trigger_px_type,
            "tpOrdPx": tp_ord_px, "slTriggerPx": sl_trigger_px,
            "slTriggerPxType": sl_trigger_px_type, "slOrdPx": sl_ord_px,
        }
        return self._http.post(c.PLACE_ALGO_ORDER, params)

    def cancel_algo_order(self, algo_id: str, inst_id: str) -> dict:
        """Cancel a single algo order.

        Args:
            algo_id: Exchange-assigned algo order ID.
            inst_id: Instrument ID.

        Returns:
            Parsed API response dict.
        """
        return self._http.post(c.CANCEL_ALGOS, [{"algoId": algo_id, "instId": inst_id}])

    def cancel_multiple_algo_orders(self, orders: list[dict]) -> dict:
        """Cancel multiple algo orders in a single request.

        Args:
            orders: List of dicts, e.g.
                ``[{"algoId": "123", "instId": "BTC-JPY"}, ...]``

        Returns:
            Parsed API response dict.
        """
        return self._http.post(c.CANCEL_ALGOS, orders)

    def get_algo_order_details(
        self,
        *,
        algo_id: str = "",
        algo_cl_ord_id: str = "",
    ) -> dict:
        """Retrieve details for a single algo order.

        Args:
            algo_id:      Exchange algo order ID.
            algo_cl_ord_id: Client algo order ID.

        Returns:
            Parsed API response dict.
        """
        params = {"algoId": algo_id, "algoClOrdId": algo_cl_ord_id}
        return self._http.get(c.GET_ALGO_ORDER_DETAILS, params)

    def amend_algo_order(
        self,
        *,
        inst_id: str = "",
        algo_id: str = "",
        algo_cl_ord_id: str = "",
        cxl_on_fail: str = "",
        req_id: str = "",
        new_sz: str = "",
        new_tp_trigger_px: str = "",
        new_tp_ord_px: str = "",
        new_sl_trigger_px: str = "",
        new_sl_ord_px: str = "",
        new_tp_trigger_px_type: str = "",
        new_sl_trigger_px_type: str = "",
    ) -> dict:
        """Amend an existing algo order.

        Returns:
            Parsed API response dict.
        """
        params = {
            "instId": inst_id, "algoId": algo_id, "algoClOrdId": algo_cl_ord_id,
            "cxlOnFail": cxl_on_fail, "reqId": req_id, "newSz": new_sz,
            "newTpTriggerPx": new_tp_trigger_px, "newTpOrdPx": new_tp_ord_px,
            "newSlTriggerPx": new_sl_trigger_px, "newSlOrdPx": new_sl_ord_px,
            "newTpTriggerPxType": new_tp_trigger_px_type,
            "newSlTriggerPxType": new_sl_trigger_px_type,
        }
        return self._http.post(c.AMEND_ALGO_ORDER, params)

    def get_algo_order_list(
        self,
        *,
        ord_type: str = "",
        algo_id: str = "",
        inst_type: str = "",
        inst_id: str = "",
        after: str = "",
        before: str = "",
        limit: str = "",
        algo_cl_ord_id: str = "",
    ) -> dict:
        """Retrieve the list of pending (unfilled) algo orders.

        Returns:
            Parsed API response dict.
        """
        params = {
            "ordType": ord_type, "algoId": algo_id,
            "instType": inst_type, "instId": inst_id,
            "after": after, "before": before, "limit": limit,
            "algoClOrdId": algo_cl_ord_id,
        }
        return self._http.get(c.ORDERS_ALGO_PENDING, params)

    def get_algo_order_history(
        self,
        ord_type: str,
        *,
        state: str = "",
        algo_id: str = "",
        inst_type: str = "",
        inst_id: str = "",
        after: str = "",
        before: str = "",
        limit: str = "",
    ) -> dict:
        """Retrieve historical algo orders.

        Args:
            ord_type: Algo type — ``"conditional"``, ``"oco"``, ``"trigger"``, etc.

        Returns:
            Parsed API response dict.
        """
        params = {
            "ordType": ord_type, "state": state, "algoId": algo_id,
            "instType": inst_type, "instId": inst_id,
            "after": after, "before": before, "limit": limit,
        }
        return self._http.get(c.ORDERS_ALGO_HISTORY, params)
