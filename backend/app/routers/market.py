from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from ..ib_client import ib_service
from ..security import require_api_key
from ..models.schemas import (
    SymbolRecord,
    QuoteRecord,
    BarRecord,
    PositionRecord,
    PnLRecord,
)


router = APIRouter(prefix="/api/v1", tags=["market"], dependencies=[Depends(require_api_key)])


@router.get("/symbols", response_model=List[SymbolRecord])
def search_symbols(query: str = Query(min_length=1, description="Symbol search string, e.g., 'AAPL'")):
    return ib_service.search_symbols(query)


@router.get("/quotes", response_model=QuoteRecord)
def get_quote(
    symbol: str = Query(description="Ticker symbol, e.g., AAPL"),
    exchange: str = Query(default="SMART"),
    currency: str = Query(default="USD"),
):
    return ib_service.get_quote(symbol=symbol, exchange=exchange, currency=currency)


@router.get("/history", response_model=List[BarRecord])
def get_history(
    symbol: str = Query(description="Ticker symbol, e.g., AAPL"),
    duration: str = Query(default="1 D", description="IB duration string, e.g., '1 D', '1 W', '1 M', '1 Y'"),
    barSize: str = Query(default="1 min", description="IB bar size, e.g., '1 min', '5 mins', '1 hour', '1 day'"),
    whatToShow: str = Query(default="TRADES", description="TRADES, MIDPOINT, BID, ASK, etc."),
    useRTH: bool = Query(default=True, description="Use regular trading hours"),
    exchange: str = Query(default="SMART"),
    currency: str = Query(default="USD"),
):
    return ib_service.get_history(
        symbol=symbol,
        duration=duration,
        bar_size=barSize,
        what_to_show=whatToShow,
        use_rth=useRTH,
        exchange=exchange,
        currency=currency,
    )


@router.get("/positions", response_model=List[PositionRecord])
def get_positions():
    return ib_service.get_positions()


@router.get("/pnl", response_model=PnLRecord)
def get_pnl(account: Optional[str] = None):
    data = ib_service.get_account_pnl(account=account)
    # Coerce values to float where applicable
    for k in ("UnrealizedPnL", "RealizedPnL", "NetLiquidation"):
        if k in data and data[k] is not None:
            try:
                data[k] = float(data[k])
            except Exception:
                pass
    return data


