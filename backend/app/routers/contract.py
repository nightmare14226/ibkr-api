from typing import Any, Dict, List, Optional

import httpx
from fastapi import APIRouter, Body, Query

from ..config import settings
from ..models.contract import (
    ContractRulesRequest,
    SecdefRecord,
    SecdefRequest,
    SecdefSearchRequest,
    StrikesResponse,
    TradingScheduleResponse,
)


router = APIRouter(tags=["contract"])


@router.get("/trsrv/secdef/schedule", response_model=TradingScheduleResponse)
async def get_trading_schedule(
    assetClass: str = Query(
        ...,
        description=(
            "Asset class of the contract. Examples: STK, OPT, FUT, CFD, WAR, SWP, FND, "
            "BND, ICS"
        ),
    ),
    symbol: str = Query(
        ...,
        description="Underlying symbol for the contract, e.g. 'AAPL'.",
    ),
    exchange: Optional[str] = Query(
        None,
        description="Native exchange for the contract, e.g. 'NASDAQ'.",
    ),
    exchangeFilter: Optional[str] = Query(
        None,
        description="Filter the response to a specific exchange.",
    ),
):
    """Fetch trading schedule details for a symbol.

    Mirrors the Client Portal API endpoint `/trsrv/secdef/schedule`.
    """

    params = {
        "assetClass": assetClass,
        "symbol": symbol,
    }
    if exchange is not None:
        params["exchange"] = exchange
    if exchangeFilter is not None:
        params["exchangeFilter"] = exchangeFilter

    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(
            f"{settings.ib_gateway_url}/trsrv/secdef/schedule",
            params=params,
        )
        response.raise_for_status()
        return response.json()


@router.post("/trsrv/secdef", response_model=List[SecdefRecord])
async def get_security_definitions(request: SecdefRequest = Body(...)):
    """Fetch security definitions for specific contract identifiers."""

    payload = {"conids": request.conids}
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(
            f"{settings.ib_gateway_url}/trsrv/secdef",
            json=payload,
        )
        response.raise_for_status()
        return response.json()


@router.get("/trsrv/futures", response_model=Dict[str, Any])
async def get_futures_contracts(symbols: str = Query(..., description="Comma separated symbols")):
    """Retrieve non-expired futures contracts for the provided symbols."""

    params = {"symbols": symbols}
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(
            f"{settings.ib_gateway_url}/trsrv/futures",
            params=params,
        )
        response.raise_for_status()
        return response.json()


@router.get("/trsrv/stocks", response_model=Dict[str, Any])
@router.get("/iserver/contract/{conid}/info", response_model=Dict[str, Any])
async def get_contract_info(conid: str):
    """Retrieve contract details for a specific conid."""

    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(
            f"{settings.ib_gateway_url}/iserver/contract/{conid}/info"
        )
        response.raise_for_status()
        return response.json()


@router.post("/iserver/secdef/search", response_model=List[Dict[str, Any]])
async def search_secdef(body: SecdefSearchRequest = Body(...)):
    """Search for securities by symbol or company name."""

    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(
            f"{settings.ib_gateway_url}/iserver/secdef/search",
            json=body.model_dump(by_alias=True, exclude_none=True),
        )
        response.raise_for_status()
        return response.json()


@router.get("/iserver/secdef/strikes", response_model=StrikesResponse)
async def get_secdef_strikes(
    conid: str = Query(..., description="Underlying contract id"),
    sectype: str = Query(..., description="Option/Warrant type"),
    month: str = Query(..., description="Contract month"),
    exchange: Optional[str] = Query(None, description="Exchange, default SMART"),
):
    params: Dict[str, Any] = {"conid": conid, "sectype": sectype, "month": month}
    if exchange:
        params["exchange"] = exchange

    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(
            f"{settings.ib_gateway_url}/iserver/secdef/strikes",
            params=params,
        )
        response.raise_for_status()
        return response.json()


@router.get("/iserver/secdef/info", response_model=List[Dict[str, Any]])
async def get_secdef_info(
    conid: str = Query(..., description="Underlying contract id"),
    sectype: str = Query(..., description="Security type"),
    month: Optional[str] = Query(None, description="Contract month (MMMYY)"),
    exchange: Optional[str] = Query(None, description="Exchange, default SMART"),
    strike: Optional[float] = Query(None, description="Strike price for options/warrants"),
    right: Optional[str] = Query(None, description="Option right: C or P"),
):
    params: Dict[str, Any] = {"conid": conid, "sectype": sectype}
    if month is not None:
        params["month"] = month
    if exchange is not None:
        params["exchange"] = exchange
    if strike is not None:
        params["strike"] = strike
    if right is not None:
        params["right"] = right

    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(
            f"{settings.ib_gateway_url}/iserver/secdef/info",
            params=params,
        )
        response.raise_for_status()
        return response.json()


@router.get("/iserver/contract/{conid}/algos", response_model=List[Dict[str, Any]])
async def get_contract_algos(
    conid: str,
    algos: Optional[str] = Query(None, description="Semicolon separated algo ids"),
    addDescription: Optional[str] = Query(None, description="Include descriptions (1/0)"),
    addParams: Optional[str] = Query(None, description="Include parameters (1/0)"),
):
    params: Dict[str, Any] = {}
    if algos is not None:
        params["algos"] = algos
    if addDescription is not None:
        params["addDescription"] = addDescription
    if addParams is not None:
        params["addParams"] = addParams

    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(
            f"{settings.ib_gateway_url}/iserver/contract/{conid}/algos",
            params=params or None,
        )
        response.raise_for_status()
        return response.json()


@router.post("/iserver/contract/rules", response_model=Dict[str, Any])
async def get_contract_rules(body: ContractRulesRequest = Body(...)):
    """Retrieve trading rules for a contract."""

    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(
            f"{settings.ib_gateway_url}/iserver/contract/rules",
            json=body.model_dump()
        )
        response.raise_for_status()
        return response.json()


@router.get("/iserver/contract/{conid}/info-and-rules", response_model=Dict[str, Any])
async def get_contract_info_and_rules(
    conid: str,
    isBuy: bool = Query(..., description="True for buy, false for sell"),
):
    params = {"isBuy": isBuy}
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(
            f"{settings.ib_gateway_url}/iserver/contract/{conid}/info-and-rules",
            params=params,
        )
        response.raise_for_status()
        return response.json()

async def get_stock_contracts(symbols: str = Query(..., description="Comma separated symbols")):
    """Retrieve stock contracts for the provided symbols."""

    params = {"symbols": symbols}
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(
            f"{settings.ib_gateway_url}/trsrv/stocks",
            params=params,
        )
        response.raise_for_status()
        return response.json()


