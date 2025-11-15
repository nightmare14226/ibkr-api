from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .config import settings
from .routers.market import router as market_router
from .routers.portfolio import router as portfolio_router
from .routers.contract import router as contract_router
from .routers.auth import router as auth_router
from .middleware.bearer import BearerAuthMiddleware
from .core.database import init_db, close_db


# Load environment variables from .env if present
load_dotenv()

app = FastAPI(title="BSD IBKR Gateway", version="0.1.0")


@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup."""
    await init_db()


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connections on application shutdown."""
    await close_db()

# Auth middleware (POST endpoints require Bearer tokens except login)
app.add_middleware(
    BearerAuthMiddleware,
    excluded_paths={"/auth/login"},
)
# CORS
origins = [o.strip() for o in settings.allowed_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "gateway_url": settings.ib_gateway_url,
    }


app.include_router(market_router)
app.include_router(portfolio_router)
app.include_router(contract_router)
app.include_router(auth_router)


