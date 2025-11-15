# main.py
from fastapi import FastAPI

from .database import Base, engine
from .models import Portfolio, Position  # noqa: F401 (ensure models are imported)
from .routers import portfolios

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Portfolio API")

app.include_router(portfolios.router)
