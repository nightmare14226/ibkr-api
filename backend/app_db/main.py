# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .models import Portfolio, Position  # noqa: F401 (ensure models are imported)
from .routers import portfolios, powerbi

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Portfolio API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(portfolios.router)
app.include_router(powerbi.router)