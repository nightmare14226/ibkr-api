from typing import List, Optional, Dict, Any

from fastapi import APIRouter, Query, Body
import httpx

from ..config import settings
from ..models.market import (
    SymbolRecord,
    QuoteRecord,
    BarRecord,
)


router = APIRouter(prefix="/iserver", tags=["market"])


@router.post("/secdef/search", response_model=List[SymbolRecord])
async def search_symbols(
    symbol: str = Body(..., description="Symbol search string, e.g., 'AAPL'"),
    secType: Optional[str] = Body(default="STK", description="Security type"),
    name: Optional[bool] = Body(default=True, description="Match by name"),
):
    """
    Search for securities/contracts by symbol.
    IB API: /iserver/secdef/search
    """
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(
            f"{settings.ib_gateway_url}/iserver/secdef/search",
            json={"symbol": symbol, "secType": secType, "name": name},
        )
        response.raise_for_status()
        return response.json()


@router.get("/secdef/info", response_model=Dict[str, Any])
async def get_contract_info(
    conid: str = Query(..., description="Contract ID (conid)"),
):
    """
    Get contract information/details.
    IB API: /iserver/secdef/info
    """
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(
            f"{settings.ib_gateway_url}/iserver/secdef/info",
            params={"conid": conid},
        )
        response.raise_for_status()
        return response.json()


@router.post("/marketdata/snapshot", response_model=QuoteRecord)
async def get_market_data_snapshot(
    conids: str = Body(..., description="Comma-separated contract IDs (conids)"),
    fields: Optional[str] = Body(default="31,84,86,88", description="Market data fields"),
):
    """
    Get market data snapshot for specified contracts.
    IB API: /iserver/marketdata/snapshot
    """
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(
            f"{settings.ib_gateway_url}/iserver/marketdata/snapshot",
            json={"conids": conids, "fields": fields},
        )
        response.raise_for_status()
        return response.json()


@router.post("/marketdata/subscribe")
async def subscribe_market_data(
    conids: str = Body(..., description="Comma-separated contract IDs (conids)"),
    fields: Optional[str] = Body(default="31,84,86,88", description="Market data fields"),
):
    """
    Subscribe to market data for specified contracts.
    IB API: /iserver/marketdata/subscribe
    """
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(
            f"{settings.ib_gateway_url}/iserver/marketdata/subscribe",
            json={"conids": conids, "fields": fields},
        )
        response.raise_for_status()
        return response.json()


@router.post("/marketdata/unsubscribe")
async def unsubscribe_market_data(
    conids: str = Body(..., description="Comma-separated contract IDs (conids) to unsubscribe"),
):
    """
    Unsubscribe from market data for specified contracts.
    IB API: /iserver/marketdata/unsubscribe
    """
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(
            f"{settings.ib_gateway_url}/iserver/marketdata/unsubscribe",
            json={"conids": conids},
        )
        response.raise_for_status()
        return response.json()


@router.get("/marketdata/history", response_model=List[BarRecord])
async def get_historical_data(
    conid: str = Query(..., description="Contract ID (conid)"),
    period: str = Query(default="1d", description="Period, e.g., '1d', '1w', '1m', '1y'"),
    bar: str = Query(default="1min", description="Bar size, e.g., '1min', '5min', '1hour', '1day'"),
    exchange: Optional[str] = Query(default=None, description="Exchange"),
    outsideRth: Optional[bool] = Query(default=False, description="Include outside regular trading hours"),
):
    """
    Get historical market data.
    IB API: /iserver/marketdata/history
    """
    async with httpx.AsyncClient(verify=False) as client:
        params = {"conid": conid, "period": period, "bar": bar, "outsideRth": outsideRth}
        if exchange:
            params["exchange"] = exchange
        response = await client.get(
            f"{settings.ib_gateway_url}/iserver/marketdata/history",
            params=params,
        )
        response.raise_for_status()
        return response.json()


@router.get("/marketdata/{conid}/unsubscribeall")
async def unsubscribe_all_market_data(conid: str):
    """
    Unsubscribe from all market data for a specific contract.
    IB API: /iserver/marketdata/{conid}/unsubscribeall
    """
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(
            f"{settings.ib_gateway_url}/iserver/marketdata/{conid}/unsubscribeall",
        )
        response.raise_for_status()
        return response.json()


