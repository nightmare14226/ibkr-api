from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class AccountParent(BaseModel):
    mmc: List[str] = Field(default_factory=list)
    accountId: str = ""
    isMParent: bool = False
    isMChild: bool = False
    isMultiplex: bool = False


class AccountRecord(BaseModel):
    id: Optional[str] = None
    accountId: str
    accountVan: Optional[str] = None
    accountTitle: Optional[str] = None
    displayName: Optional[str] = None
    accountAlias: Optional[str] = None
    accountStatus: Optional[int] = None
    currency: Optional[str] = None
    type: Optional[str] = None
    tradingType: Optional[str] = None
    businessType: Optional[str] = None
    category: Optional[str] = None
    ibEntity: Optional[str] = None
    clearingStatus: Optional[str] = None
    acctCustType: Optional[str] = None
    desc: Optional[str] = None
    # Boolean fields with defaults
    brokerageAccess: Optional[bool] = None
    faclient: Optional[bool] = None
    covestor: Optional[bool] = None
    noClientTrading: Optional[bool] = None
    trackVirtualFXPortfolio: Optional[bool] = None
    # Fields with hyphens - using extra fields
    parent: Optional[AccountParent] = None
    
    class Config:
        populate_by_name = True
        extra = "allow"  # Allow extra fields like "PrepaidCrypto-Z", "PrepaidCrypto-P"


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


class AccountSummaryRecord(BaseModel):
    account: str
    tag: str
    value: str
    currency: Optional[str] = None


class AccountLedgerRecord(BaseModel):
    commoditymarketvalue: Optional[float] = None
    futuremarketvalue: Optional[float] = None
    settledcash: Optional[float] = None
    exchangerate: Optional[float] = None
    sessionid: Optional[int] = None
    cashbalance: Optional[float] = None
    corporatebondsmarketvalue: Optional[float] = None
    warrantsmarketvalue: Optional[float] = None
    netliquidationvalue: Optional[float] = None
    interest: Optional[float] = None
    unrealizedpnl: Optional[float] = None
    stockmarketvalue: Optional[float] = None
    moneyfunds: Optional[float] = None
    currency: str
    realizedpnl: Optional[float] = None
    funds: Optional[float] = None
    acctcode: Optional[str] = None
    issueroptionsmarketvalue: Optional[float] = None
    key: Optional[str] = None
    timestamp: Optional[int] = None
    severity: Optional[int] = None
    stockoptionmarketvalue: Optional[float] = None
    futuresonlypnl: Optional[float] = None
    tbondsmarketvalue: Optional[float] = None
    futureoptionmarketvalue: Optional[float] = None
    cashbalancefxsegment: Optional[float] = None
    secondkey: Optional[str] = None
    tbillsmarketvalue: Optional[float] = None
    endofbundle: Optional[int] = None
    dividends: Optional[float] = None
    cryptocurrencyvalue: Optional[float] = None
    
    class Config:
        extra = "allow"

