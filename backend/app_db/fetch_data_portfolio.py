import requests
from dataclasses import dataclass
from typing import Dict, List, Optional

# ==========================
# CONFIG
# ==========================

BASE_URL = "https://localhost:5000/v1/api"   # change if needed
VERIFY_SSL = False                           # often False for local CP gateway

# Your watchlist / subset (optional). If empty, all positions are pulled.
WATCHLIST = {
    "AMAT", "AMZN", "ANET", "AVGO", "ESTC", "GOOGL", "INTC", "KEYS",
    "META", "MNDY", "MRVL", "MSFT", "ORCL", "PYPL", "SAP", "SNOW",
    "TSM", "WDAY",
}


# ==========================
# DATA MODEL
# ==========================

@dataclass
class PositionRow:
    symbol: str
    name: Optional[str]
    quantity: float
    last_price: Optional[float]
    avg_cost: Optional[float]
    market_value: Optional[float]
    weight_pct: Optional[float]        # 0.0967 for 9.67%
    unrealized_pnl_pct: Optional[float]  # 2.5273 for 252.73%
    daily_change_pct: Optional[float]  # 0.0125 for 1.25%
    perf_30d: Optional[float]          # 0.191 for +19.1%
    perf_60d: Optional[float]
    currency: str
    pe_ratio: Optional[float]


# ==========================
# CLIENT
# ==========================

class IBClient:
    def __init__(self, base_url: str, verify_ssl: bool = True):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.verify = verify_ssl

    def _get(self, path: str, **kwargs):
        url = f"{self.base_url}{path}"
        resp = self.session.get(url, **kwargs)
        resp.raise_for_status()
        return resp.json()

    # ---- Accounts ----
    def get_accounts(self) -> List[Dict]:
        return self._get("/portfolio/accounts")

    def get_primary_account_id(self) -> str:
        accounts = self.get_accounts()
        if not accounts:
            raise RuntimeError("No IBKR accounts returned from /portfolio/accounts")
        # pick first; adjust if you need specific account
        return accounts[0]["accountId"]

    # ---- Positions ----
    def get_positions(self, account_id: str) -> List[Dict]:
        # 0 = first page. For large accounts you might need to increment page id.
        return self._get(f"/portfolio/{account_id}/positions/0")

    # ---- Snapshot market data ----
    def get_snapshot(
        self, conids: List[int], fields: List[int]
    ) -> Dict[int, Dict[str, str]]:
        """
        Returns dict: conid -> { field_id_str: value_str, ... }
        """
        if not conids:
            return {}

        params = {
            "conids": ",".join(str(c) for c in conids),
            "fields": ",".join(str(f) for f in fields),
        }
        data = self._get("/iserver/marketdata/snapshot", params=params)

        by_conid: Dict[int, Dict[str, str]] = {}
        for item in data:
            c = item.get("conid")
            if c is None:
                continue
            # item is like {"conid": 12345, "31": "226.01", "55": "AMAT", ...}
            by_conid[int(c)] = item
        return by_conid

    # ---- History for perf ----
    def get_history_daily(self, conid: int, period: str = "60d") -> List[Dict]:
        """
        Returns list of bars (dicts) for given conid.
        """
        params = {
            "conid": conid,
            "period": period,  # "60d"
            "bar": "1d",
        }
        try:
            data = self._get("/iserver/marketdata/history", params=params)
        except requests.HTTPError as e:
            print(f"History error for {conid}: {e}")
            return []

        # spec: data["data"] is list of { "c": close, "o": open, "h": high, "l": low, "t": timestamp }
        return data.get("data", [])


# ==========================
# UTIL
# ==========================

def safe_float(x) -> Optional[float]:
    if x is None:
        return None
    try:
        return float(x)
    except (ValueError, TypeError):
        return None


def compute_perf_from_bars(bars: List[Dict], days: int) -> Optional[float]:
    """
    bars: list of daily bars, oldest -> newest or newest -> oldest depending on IB.
    IB usually returns ascending by time, but verify with your data.
    We'll assume ascending: bars[0] = oldest, bars[-1] = latest.
    Returns (P0 / P_old - 1) or None if not enough data.
    """
    if not bars or len(bars) <= days:
        return None

    # ensure we have enough bars
    latest_bar = bars[-1]
    old_bar = bars[-1 - days]

    c0 = safe_float(latest_bar.get("c"))
    c_old = safe_float(old_bar.get("c"))
    if c0 is None or c_old is None or c_old == 0:
        return None

    return c0 / c_old - 1.0


# ==========================
# MAIN LOGIC
# ==========================

def build_portfolio_table(client: IBClient) -> List[PositionRow]:
    account_id = client.get_primary_account_id()
    positions = client.get_positions(account_id)

    # Filter by watchlist symbols if provided:
    filtered_positions = []
    for p in positions:
        symbol = p.get("ticker") or p.get("contractDesc") or p.get("symbol")
        # positions endpoint usually has "conid", "position", "avgPrice", "currency"
        if WATCHLIST and symbol not in WATCHLIST:
            continue
        filtered_positions.append(p)

    conids = [int(p["conid"]) for p in filtered_positions]

    # Snapshot fields we care about:
    field_ids = [
        31,    # Last Price
        55,    # Symbol
        73,    # Market Value
        74,    # Avg Price
        75,    # Unrealized PnL (money)
        80,    # Unrealized PnL %
        83,    # Change %
        7051,  # Company name
        7290,  # P/E
        7639,  # % of Mark Value
    ]

    snapshot_by_conid = client.get_snapshot(conids, field_ids)

    rows: List[PositionRow] = []

    for p in filtered_positions:
        conid = int(p["conid"])
        snap = snapshot_by_conid.get(conid, {})

        symbol = snap.get("55") or p.get("ticker") or p.get("contractDesc") or ""
        quantity = safe_float(p.get("position")) or 0.0
        currency = p.get("currency", "")

        last_price = safe_float(snap.get("31"))
        avg_cost = safe_float(snap.get("74"))
        market_value = safe_float(snap.get("73"))

        # 7639 is "% of Mark Value" as percentage
        weight_pct = safe_float(snap.get("7639"))
        if weight_pct is not None:
            weight_pct /= 100.0  # convert "9.67" -> 0.0967

        unreal_pnl_pct = safe_float(snap.get("80"))
        if unreal_pnl_pct is not None:
            unreal_pnl_pct /= 100.0  # convert "252.73" -> 2.5273

        daily_change_pct = safe_float(snap.get("83"))
        if daily_change_pct is not None:
            daily_change_pct /= 100.0  # "1.25" -> 0.0125

        name = snap.get("7051")
        pe_ratio = safe_float(snap.get("7290"))

        # ---- History for 30D / 60D perf ----
        bars = client.get_history_daily(conid, period="60d")
        perf_30d = compute_perf_from_bars(bars, 30)
        perf_60d = compute_perf_from_bars(bars, 60)

        row = PositionRow(
            symbol=symbol,
            name=name,
            quantity=quantity,
            last_price=last_price,
            avg_cost=avg_cost,
            market_value=market_value,
            weight_pct=weight_pct,
            unrealized_pnl_pct=unreal_pnl_pct,
            daily_change_pct=daily_change_pct,
            perf_30d=perf_30d,
            perf_60d=perf_60d,
            currency=currency,
            pe_ratio=pe_ratio,
        )
        rows.append(row)

    return rows


if __name__ == "__main__":
    client = IBClient(BASE_URL, verify_ssl=VERIFY_SSL)
    rows = build_portfolio_table(client)

    # Pretty-print
    header = (
        "Symbol  Qty     Last      AvgCost   Value       Weight   U_PnL%  "
        "DayChg%  Perf30D  Perf60D  Curr  P/E    Name"
    )
    print(header)
    print("-" * len(header))
    for r in rows:
        print(
            f"{r.symbol:<6} "
            f"{r.quantity:<7.2f} "
            f"{(r.last_price or 0):<9.2f} "
            f"{(r.avg_cost or 0):<8.2f} "
            f"{(r.market_value or 0):<10.2f} "
            f"{(r.weight_pct or 0):<7.4f} "
            f"{(r.unrealized_pnl_pct or 0):<7.4f} "
            f"{(r.daily_change_pct or 0):<7.4f} "
            f"{(r.perf_30d or 0):<8.4f} "
            f"{(r.perf_60d or 0):<8.4f} "
            f"{r.currency:<4} "
            f"{(r.pe_ratio or 0):<6.2f} "
            f"{(r.name or '')}"
        )
