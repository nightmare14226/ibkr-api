import requests
from datetime import datetime
import pytz

BASE_URL = "https://localhost:5000/v1/api"
TZ_NAME = "America/New_York"  # IBKR statements usually use EST/EDT

session = requests.Session()
session.verify = False  # because IBKR gateway uses self-signed TLS


def format_period_and_generated_from_ms(ts_ms: int, tz_name: str = TZ_NAME):
    """
    Convert IBKR millisecond timestamp to:
      - period: date only (MM/DD/YYYY)
      - generated: full datetime (YYYY-MM-DD, HH:MM:SS Z)
    using the given timezone.
    """
    ts_sec = ts_ms / 1000.0
    tz = pytz.timezone(tz_name)
    dt = datetime.fromtimestamp(ts_sec, tz)

    period = dt.strftime("%m/%d/%Y")                # e.g. 11/12/2025
    generated = dt.strftime("%Y-%m-%d, %H:%M:%S %Z")  # e.g. 2025-11-13, 02:54:34 EST
    return period, generated


def get_account_header_from_meta_and_ledger(account_id: str):
    # 1) /meta -> name, account, customer type, base currency
    r_meta = session.get(f"{BASE_URL}/portfolio/{account_id}/meta")
    r_meta.raise_for_status()
    meta = r_meta.json()

    name = meta.get("accountTitle") or meta.get("displayName")
    account = meta.get("accountId") or meta.get("id")
    customer_type = meta.get("type")                 # e.g. "INDIVIDUAL"
    account_type = meta.get("acctCustType")          # e.g. "IRA-Tax Free Savings Account/Canada"
    base_currency_from_meta = meta.get("currency")   # backup

    # 2) /ledger -> cash, portfolio (net liquidation), timestamp, base currency
    r_ledger = session.get(f"{BASE_URL}/portfolio/{account_id}/ledger")
    r_ledger.raise_for_status()
    ledger = r_ledger.json()

    base = ledger["BASE"]

    cash = base["cashbalance"]                       # full cash in base currency
    portfolio = base["netliquidationvalue"]          # total portfolio value in base currency
    base_currency = base.get("currency") or base_currency_from_meta

    ts_ms = base.get("timestamp", 0)
    period, generated = ("", "")
    if ts_ms and ts_ms > 0:
        period, generated = format_period_and_generated_from_ms(ts_ms)
    else:
        # fallback if ledger timestamp is missing; you could also call /summary here if needed
        period, generated = ("", "")

    return {
        "period": period,
        "generated": generated,
        "name": name,
        "account": account,
        "customerType": customer_type,
        "accountType": account_type,
        "baseCurrency": base_currency,
        "cash": cash,
        "portfolio": portfolio,
    }


if __name__ == "__main__":
    header = get_account_header_from_meta_and_ledger("U10322314")
    print(header)
