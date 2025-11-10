from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class TradingSession(BaseModel):
    openingTime: Optional[int] = None
    closingTime: Optional[int] = None
    prop: Optional[str] = None


class TradingTimes(BaseModel):
    openingTime: Optional[int] = None
    closingTime: Optional[int] = None
    cancelDayOrders: Optional[str] = None


class TradingScheduleItem(BaseModel):
    clearingCycleEndTime: Optional[int] = None
    tradingScheduleDate: Optional[int] = None
    sessions: Optional[TradingSession] = None
    tradingTimes: Optional[TradingTimes] = None


class TradingScheduleResponse(BaseModel):
    id: Optional[str] = None
    tradeVenueId: Optional[str] = None
    schedules: List[TradingScheduleItem] = Field(default_factory=list)


class SecdefRequest(BaseModel):
    conids: List[int] = Field(..., description="Contract identifiers")


class SecdefSearchRequest(BaseModel):
    symbol: str
    name: Optional[bool] = Field(default=False, description="Search by company name")
    secType: Optional[str] = Field(default=None, description="Security type filter")


class IncrementRules(BaseModel):
    lowerEdge: Optional[float] = None
    increment: Optional[float] = None


class SecdefRecord(BaseModel):
    conid: Optional[int] = None
    currency: Optional[str] = None
    crossCurrency: Optional[bool] = None
    time: Optional[int] = None
    chineseName: Optional[str] = None
    allExchanges: Optional[str] = None
    listingExchange: Optional[str] = None
    name: Optional[str] = None
    assetClass: Optional[str] = None
    expiry: Optional[str] = None
    lastTradingDay: Optional[str] = None
    group: Optional[str] = None
    putOrCall: Optional[str] = None
    sector: Optional[str] = None
    sectorGroup: Optional[str] = None
    strike: Optional[float] = None
    ticker: Optional[str] = None
    undConid: Optional[int] = None
    multiplier: Optional[int] = None
    type: Optional[str] = None
    undComp: Optional[str] = None
    undSym: Optional[str] = None
    hasOptions: Optional[bool] = None
    fullName: Optional[str] = None
    isUS: Optional[bool] = None
    incrementRules: Optional[IncrementRules] = None


class StrikesResponse(BaseModel):
    call: List[str] = Field(default_factory=list)
    put: List[str] = Field(default_factory=list)


class ContractRulesRequest(BaseModel):
    conid: str
    isBuy: bool


