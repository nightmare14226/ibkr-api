from __future__ import annotations

from threading import Lock
from typing import Any, Dict, List, Optional

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from ib_insync import IB, Stock, Contract, util

from .config import settings


class IBService:
    """Thread-safe singleton wrapper around ib_insync.IB with basic helpers."""

    _instance: Optional["IBService"] = None
    _instance_lock: Lock = Lock()

    def __init__(self) -> None:
        self._ib = IB()
        self._lock = Lock()

    @classmethod
    def instance(cls) -> "IBService":
        if not cls._instance:
            with cls._instance_lock:
                if not cls._instance:
                    cls._instance = IBService()
        return cls._instance

    def is_connected(self) -> bool:
        return self._ib.isConnected()

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=0.5, min=1, max=8),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    def connect(self) -> None:
        with self._lock:
            if self._ib.isConnected():
                return
            self._ib.connect(settings.ib_host, settings.ib_port, clientId=settings.ib_client_id)

    def ensure_connected(self) -> None:
        if not self._ib.isConnected():
            self.connect()

    # ---------- Helpers ----------
    def qualify_stock(self, symbol: str, exchange: str = "SMART", currency: str = "USD") -> Contract:
        self.ensure_connected()
        contract = Stock(symbol, exchange, currency)
        qualified = self._ib.qualifyContracts(contract)
        if not qualified:
            raise ValueError(f"Unable to qualify contract for symbol={symbol}")
        return qualified[0]

    def search_symbols(self, query: str) -> List[Dict[str, Any]]:
        self.ensure_connected()
        results = self._ib.reqMatchingSymbols(query)
        # Normalize to JSON-friendly dicts
        out: List[Dict[str, Any]] = []
        for r in results:
            desc = r.contract
            out.append(
                {
                    "conId": desc.conId,
                    "symbol": desc.symbol,
                    "secType": desc.secType,
                    "currency": desc.currency,
                    "exchange": desc.exchange,
                    "primaryExchange": desc.primaryExchange,
                    "description": r.derivativeSecTypes,
                }
            )
        return out

    def get_quote(self, symbol: str, exchange: str = "SMART", currency: str = "USD") -> Dict[str, Any]:
        self.ensure_connected()
        contract = self.qualify_stock(symbol, exchange, currency)
        [ticker] = self._ib.reqTickers(contract)
        # Convert to dict; use util for robust conversion
        data = util.tree(ticker)
        # Pick commonly used fields for Power BI; keep raw for completeness
        return {
            "symbol": symbol,
            "bid": getattr(ticker, "bid", None),
            "ask": getattr(ticker, "ask", None),
            "last": getattr(ticker, "last", None),
            "close": getattr(ticker, "close", None),
            "time": util.formatIBDatetime(getattr(ticker, "time", None)) if getattr(ticker, "time", None) else None,
            "raw": data,
        }

    def get_history(
        self,
        symbol: str,
        duration: str = "1 D",
        bar_size: str = "1 min",
        what_to_show: str = "TRADES",
        use_rth: bool = True,
        exchange: str = "SMART",
        currency: str = "USD",
    ) -> List[Dict[str, Any]]:
        self.ensure_connected()
        contract = self.qualify_stock(symbol, exchange, currency)
        bars = self._ib.reqHistoricalData(
            contract,
            endDateTime="",
            durationStr=duration,
            barSizeSetting=bar_size,
            whatToShow=what_to_show,
            useRTH=use_rth,
            formatDate=1,
        )
        out: List[Dict[str, Any]] = []
        for b in bars:
            out.append(
                {
                    "time": util.formatIBDatetime(b.date),
                    "open": float(b.open),
                    "high": float(b.high),
                    "low": float(b.low),
                    "close": float(b.close),
                    "volume": int(b.volume) if b.volume is not None else None,
                    "barCount": int(b.barCount) if getattr(b, "barCount", None) is not None else None,
                    "wap": float(b.wap) if getattr(b, "wap", None) is not None else None,
                }
            )
        return out

    def get_positions(self) -> List[Dict[str, Any]]:
        self.ensure_connected()
        positions = self._ib.positions()
        out: List[Dict[str, Any]] = []
        for p in positions:
            out.append(
                {
                    "account": p.account,
                    "conId": p.contract.conId,
                    "symbol": p.contract.symbol,
                    "secType": p.contract.secType,
                    "exchange": p.contract.exchange,
                    "currency": p.contract.currency,
                    "position": float(p.position),
                    "avgCost": float(p.avgCost) if p.avgCost is not None else None,
                }
            )
        return out

    def get_account_pnl(self, account: Optional[str] = None) -> Dict[str, Any]:
        self.ensure_connected()
        # Use account summary for realized/unrealized PnL and net liquidation
        summary = self._ib.accountSummary(account)
        data: Dict[str, Dict[str, Any]] = {}
        for item in summary:
            acct = item.account
            if acct not in data:
                data[acct] = {}
            data[acct][item.tag] = item.value
        # If account is specified, return only that
        if account:
            return {"account": account, **data.get(account, {})}
        # Otherwise return the first account (common single-account setup)
        if data:
            acct = next(iter(data.keys()))
            return {"account": acct, **data[acct]}
        return {}


ib_service = IBService.instance()

