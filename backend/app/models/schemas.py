from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class SymbolRecord(BaseModel):
    conId: int
    symbol: str
    secType: str
    currency: str
    exchange: Optional[str] = None
    primaryExchange: Optional[str] = None
    description: Optional[List[str]] = None


class QuoteRecord(BaseModel):
    symbol: str
    bid: Optional[float] = None
    ask: Optional[float] = None
    last: Optional[float] = None
    close: Optional[float] = None
    time: Optional[str] = None
    raw: Dict[str, Any] = Field(default_factory=dict)


class BarRecord(BaseModel):
    time: str
    open: float
    high: float
    low: float
    close: float
    volume: Optional[int] = None
    barCount: Optional[int] = None
    wap: Optional[float] = None


class PositionRecord(BaseModel):
    account: str
    conId: int
    symbol: str
    secType: str
    exchange: Optional[str] = None
    currency: str
    position: float
    avgCost: Optional[float] = None


class PnLRecord(BaseModel):
    account: str
    UnrealizedPnL: Optional[float] = None
    RealizedPnL: Optional[float] = None
    NetLiquidation: Optional[float] = None

