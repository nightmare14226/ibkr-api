# schemas.py
from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# ---------- Position schemas ----------

class PositionBase(BaseModel):
    symbol: str
    quantity: float

    last_price: Optional[float] = None
    avg_cost: Optional[float] = None
    value: float

    weight_pct: Optional[float] = Field(default=None, description="Weight % in portfolio")
    unrealized_pct: Optional[float] = None
    daily_change_pct: Optional[float] = None
    perf_30d_pct: Optional[float] = None
    perf_60d_pct: Optional[float] = None

    pt: Optional[float] = Field(default=None, description="Price target")
    upside_pct: Optional[float] = None

    currency: str
    equity_risk_profile: Optional[str] = None
    name: str
    pe_ratio: Optional[float] = None


class PositionCreate(PositionBase):
    pass


class PositionRead(PositionBase):
    id: int

    class Config:
        from_attributes = True


# ---------- Portfolio schemas ----------

class PortfolioBase(BaseModel):
    # header
    period: date
    generated_at: datetime
    owner_name: str
    account: str
    customer_type: str
    base_currency: str

    cash: float
    portfolio_value: float

    # metrics
    account_type: Optional[str] = None

    accrued_cash: Optional[float] = None
    accruedcash: Optional[float] = None

    available_funds: Optional[float] = None
    availablefunds: Optional[float] = None

    buying_power: Optional[float] = None
    buyingpower: Optional[float] = None

    currency_exposure: Optional[float] = None

    cushion: Optional[float] = None
    dividend_yield: Optional[float] = None

    equities: Optional[float] = None
    equity_with_loan_value: Optional[float] = None
    equitywithloanvalue: Optional[float] = None

    excess_liquidity: Optional[float] = None
    excessliquidity: Optional[float] = None

    full_available_funds: Optional[float] = None
    full_excess_liquidity: Optional[float] = None
    full_init_margin_req: Optional[float] = None
    full_maint_margin_req: Optional[float] = None

    fullavailablefunds: Optional[float] = None
    fullexcessliquidity: Optional[float] = None
    fullinitmarginreq: Optional[float] = None
    fullmaintmarginreq: Optional[float] = None

    gross_position_value: Optional[float] = None
    grosspositionvalue: Optional[float] = None

    init_margin_req: Optional[float] = None
    initmarginreq: Optional[float] = None

    look_ahead_available_funds: Optional[float] = None
    look_ahead_excess_liquidity: Optional[float] = None
    look_ahead_init_margin_req: Optional[float] = None
    look_ahead_maint_margin_req: Optional[float] = None
    look_ahead_next_change: Optional[float] = None

    lookaheadavailablefunds: Optional[float] = None
    lookaheadexcessliquidity: Optional[float] = None
    lookaheadinitmarginreq: Optional[float] = None
    lookaheadmaintmarginreq: Optional[float] = None
    lookaheadnextchange: Optional[float] = None

    maint_margin_req: Optional[float] = None
    maintmarginreq: Optional[float] = None

    net_liquidation: Optional[float] = None
    netliquidation: Optional[float] = None

    portfolio_beta: Optional[float] = None
    portfolio_volatility: Optional[float] = None

    realized_pnl: Optional[float] = None
    sharpe_ratio: Optional[float] = None

    top_holding_symbol: Optional[str] = None
    top_holding_value: Optional[float] = None

    total: Optional[float] = None
    total_cash_value: Optional[float] = None
    totalcashvalue: Optional[float] = None

    unrealized_pnl: Optional[float] = None
    ytd_return: Optional[float] = None


class PortfolioCreate(PortfolioBase):
    positions: List[PositionCreate] = []


class PortfolioRead(PortfolioBase):
    id: int
    positions: List[PositionRead] = []

    class Config:
        from_attributes = True
