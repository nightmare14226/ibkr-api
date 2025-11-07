from typing import List, Optional, Dict, Any

from fastapi import APIRouter, Query, Body
import httpx

from ..config import settings
from ..models.portfolio import (
    AccountRecord,
    PositionRecord,
    PnLRecord,
    AccountSummaryRecord,
    AccountLedgerRecord,
)


router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("/accounts", response_model=List[AccountRecord])
async def get_portfolio_accounts():
    """
    Get portfolio accounts.
    IB API: /portfolio/accounts
    """
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(f"{settings.ib_gateway_url}/portfolio/accounts")
        response.raise_for_status()
        return response.json()


@router.get("/subaccounts", response_model=List[AccountRecord])
async def get_subaccounts():
    """
    Get list of sub-accounts.
    IB API: /portfolio/subaccounts
    """
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(f"{settings.ib_gateway_url}/portfolio/subaccounts")
        response.raise_for_status()
        return response.json()


@router.get("/subaccounts2", response_model=List[AccountRecord])
async def get_subaccounts2():
    """
    Get list of sub-accounts (for large accounts).
    IB API: /portfolio/subaccounts2
    """
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(f"{settings.ib_gateway_url}/portfolio/subaccounts2")
        response.raise_for_status()
        return response.json()


@router.get("/{accountId}/meta", response_model=Dict[str, Any])
async def get_account_meta(accountId: str):
    """
    Get account information/metadata.
    IB API: /portfolio/{accountId}/meta
    """
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(f"{settings.ib_gateway_url}/portfolio/{accountId}/meta")
        response.raise_for_status()
        return response.json()


@router.get("/{accountId}/allocation", response_model=Dict[str, Any])
async def get_account_allocation(accountId: str):
    """
    Get account allocation information.
    IB API: /portfolio/{accountId}/allocation
    """
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(f"{settings.ib_gateway_url}/portfolio/{accountId}/allocation")
        response.raise_for_status()
        return response.json()


@router.post("/allocation", response_model=Dict[str, Any])
async def get_all_accounts_allocation():
    """
    Get account allocation for all accounts.
    IB API: /portfolio/allocation
    """
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(f"{settings.ib_gateway_url}/portfolio/allocation")
        response.raise_for_status()
        return response.json()


@router.get("/{accountId}/positions/{pageId}", response_model=List[PositionRecord])
async def get_portfolio_positions(
    accountId: str,
    pageId: str,
):
    """
    Get portfolio positions for an account (paginated).
    IB API: /portfolio/{accountId}/positions/{pageId}
    """
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(
            f"{settings.ib_gateway_url}/portfolio/{accountId}/positions/{pageId}"
        )
        response.raise_for_status()
        return response.json()


@router.get("/{accountId}/position/{conid}", response_model=PositionRecord)
async def get_position_by_conid(accountId: str, conid: str):
    """
    Get position by contract ID (conid) for an account.
    IB API: /portfolio/{accountId}/position/{conid}
    """
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(
            f"{settings.ib_gateway_url}/portfolio/{accountId}/position/{conid}"
        )
        response.raise_for_status()
        return response.json()


@router.post("/{accountId}/positions/invalidate")
async def invalidate_portfolio_cache(accountId: str):
    """
    Invalidate the backend cache of the Portfolio.
    IB API: /portfolio/{accountId}/positions/invalidate
    """
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(
            f"{settings.ib_gateway_url}/portfolio/{accountId}/positions/invalidate"
        )
        response.raise_for_status()
        return response.json()


@router.get("/{accountId}/summary", response_model=Dict[str, Any])
async def get_portfolio_summary(accountId: str):
    """
    Get account summary for an account.
    IB API: /portfolio/{accountId}/summary
    """
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(f"{settings.ib_gateway_url}/portfolio/{accountId}/summary")
        response.raise_for_status()
        return response.json()


@router.get("/{accountId}/ledger", response_model=Dict[str, AccountLedgerRecord])
async def get_portfolio_ledger(accountId: str):
    """
    Get account ledger for an account.
    Returns a dictionary keyed by currency (e.g., 'USD', 'BASE').
    IB API: /portfolio/{accountId}/ledger
    """
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(f"{settings.ib_gateway_url}/portfolio/{accountId}/ledger")
        response.raise_for_status()
        return response.json()


@router.get("/positions/{conid}", response_model=List[PositionRecord])
async def get_positions_by_conid(conid: str):
    """
    Get positions by contract ID (conid) across all accounts.
    IB API: /portfolio/positions/{conid}
    """
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(f"{settings.ib_gateway_url}/portfolio/positions/{conid}")
        response.raise_for_status()
        return response.json()

