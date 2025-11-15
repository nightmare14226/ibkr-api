# routers/portfolios.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Portfolio, Position
from ..schemas import PortfolioCreate, PortfolioRead

router = APIRouter(prefix="/portfolios", tags=["portfolios"])


@router.post("/", response_model=PortfolioRead)
def create_portfolio(portfolio_in: PortfolioCreate, db: Session = Depends(get_db)):
    # create Portfolio from all fields except positions
    data = portfolio_in.model_dump(exclude={"positions"})
    portfolio = Portfolio(**data)

    for pos_in in portfolio_in.positions:
        position = Position(
            symbol=pos_in.symbol,
            quantity=pos_in.quantity,
            last_price=pos_in.last_price,
            avg_cost=pos_in.avg_cost,
            value=pos_in.value,
            weight_pct=pos_in.weight_pct,
            unrealized_pct=pos_in.unrealized_pct,
            daily_change_pct=pos_in.daily_change_pct,
            perf_30d_pct=pos_in.perf_30d_pct,
            perf_60d_pct=pos_in.perf_60d_pct,
            pt=pos_in.pt,
            upside_pct=pos_in.upside_pct,
            currency=pos_in.currency,
            equity_risk_profile=pos_in.equity_risk_profile,
            name=pos_in.name,
            pe_ratio=pos_in.pe_ratio,
        )
        portfolio.positions.append(position)

    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    return portfolio


@router.get("/", response_model=List[PortfolioRead])
def list_portfolios(db: Session = Depends(get_db)):
    return db.query(Portfolio).all()


@router.get("/{portfolio_id}", response_model=PortfolioRead)
def get_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio


@router.delete("/{portfolio_id}", status_code=204)
def delete_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    db.delete(portfolio)
    db.commit()
    return
