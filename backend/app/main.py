from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .config import settings
from .routers.market import router as market_router
from .routers.portfolio import router as portfolio_router
from .routers.contract import router as contract_router


# Load environment variables from .env if present
load_dotenv()

app = FastAPI(title="BSD IBKR Gateway", version="0.1.0")

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


