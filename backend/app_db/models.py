# models.py
from typing import List, Optional

from sqlalchemy import String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date, datetime

from .database import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Header info
    period: Mapped[date] = mapped_column(Date)
    generated_at: Mapped[datetime] = mapped_column(DateTime)

    cash: Mapped[float] = mapped_column(Float)
    portfolio_value: Mapped[float] = mapped_column(Float)

    owner_name: Mapped[str] = mapped_column(String(100))
    account: Mapped[str] = mapped_column(String(32))
    customer_type: Mapped[str] = mapped_column(String(50))
    base_currency: Mapped[str] = mapped_column(String(8))

    # Summary
    cash: Mapped[float]
    portfolio_value: Mapped[float]

    # ---------- Metrics ----------
    account_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    accrued_cash: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    accruedcash: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    available_funds: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    availablefunds: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    buying_power: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    buyingpower: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    currency_exposure: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    cushion: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    dividend_yield: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    equities: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    equity_with_loan_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    equitywithloanvalue: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    excess_liquidity: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    excessliquidity: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    full_available_funds: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    full_excess_liquidity: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    full_init_margin_req: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    full_maint_margin_req: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    fullavailablefunds: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    fullexcessliquidity: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    fullinitmarginreq: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    fullmaintmarginreq: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    gross_position_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    grosspositionvalue: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    init_margin_req: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    initmarginreq: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    look_ahead_available_funds: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    look_ahead_excess_liquidity: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    look_ahead_init_margin_req: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    look_ahead_maint_margin_req: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    look_ahead_next_change: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    lookaheadavailablefunds: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    lookaheadexcessliquidity: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    lookaheadinitmarginreq: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    lookaheadmaintmarginreq: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    lookaheadnextchange: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    maint_margin_req: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    maintmarginreq: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    net_liquidation: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    netliquidation: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    portfolio_beta: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    portfolio_volatility: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    realized_pnl: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    sharpe_ratio: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    top_holding_symbol: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    top_holding_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    total: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    total_cash_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    totalcashvalue: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    unrealized_pnl: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    ytd_return: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Relations
    positions: Mapped[List["Position"]] = relationship(
        back_populates="portfolio",
        cascade="all, delete-orphan",
    )


class Position(Base):
    __tablename__ = "positions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolios.id"))

    symbol: Mapped[str] = mapped_column(String(10), index=True)
    quantity: Mapped[float]

    last_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    avg_cost: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    value: Mapped[float]

    weight_pct: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    unrealized_pct: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    daily_change_pct: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    perf_30d_pct: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    perf_60d_pct: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    pt: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    upside_pct: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    currency: Mapped[str] = mapped_column(String(8))
    equity_risk_profile: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    name: Mapped[str] = mapped_column(String(200))

    pe_ratio: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    portfolio: Mapped[Portfolio] = relationship(back_populates="positions")
