import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .config import settings
from .ib_client import ib_service
from .routers.market import router as market_router


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


@app.on_event("startup")
def on_startup() -> None:
    # Try connecting eagerly so first request is fast; rely on ensure_connected otherwise
    try:
        ib_service.connect()
    except Exception:
        # Defer connect errors to first protected call; health stays informative
        pass


@app.get("/health")
def health():
    return {
        "status": "ok",
        "ib_connected": ib_service.is_connected(),
        "host": settings.ib_host,
        "port": settings.ib_port,
    }


app.include_router(market_router)


