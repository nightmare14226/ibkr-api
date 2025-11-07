# BSD IBKR Gateway (FastAPI)

A lightweight proxy API that wraps the IB Client Portal Gateway and exposes REST endpoints that Power BI can refresh on demand.

## Features
- Proxies requests to IB Client Portal Gateway (https://localhost:5000)
- Endpoints: health, symbols search, quotes, historical bars, positions, account PnL
- JSON outputs friendly for Power BI ingestion
- Designed for self-hosting on VPS/Azure

## Prerequisites
- Python 3.11+
- IB Client Portal Gateway running and accessible (default: https://localhost:5000)

## Quick start (Windows PowerShell)
```powershell
cd backend
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy example.env .env  # then edit .env values

# Run dev server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Then open:
- http://localhost:8000/health
- http://localhost:8000/docs

## Environment variables (.env)
```
IB_GATEWAY_URL=https://localhost:5000
ALLOWED_ORIGINS=*
TIMEZONE=UTC
```

## Example endpoints
- `GET /health`
- `GET /v1/api/symbols?query=AAPL`
- `GET /v1/api/quotes?symbol=AAPL&exchange=SMART&currency=USD`
- `GET /v1/api/history?symbol=AAPL&duration=1%20D&barSize=1%20min&whatToShow=TRADES&useRTH=true`
- `GET /v1/api/positions`
- `GET /v1/api/pnl` (optional `account`)

All endpoints proxy requests to the IB Client Portal Gateway.

## Power BI setup (Desktop)
1. In Power BI Desktop, use `Get Data` -> `Web`.
2. Enter endpoint URL (e.g., `http://<server>:8000/v1/api/history?symbol=AAPL&duration=1%20M&barSize=1%20day`).
3. Transform to table, expand records as needed.
4. Parameterize `symbol`, `duration`, `barSize` and enable incremental refresh for historical tables.

## Production deployment (VPS/Azure)
- Use a process manager (e.g., `systemd`) to run `uvicorn app.main:app --host 0.0.0.0 --port 8000`.
- Put NGINX/Caddy in front for HTTPS termination.
- Restrict inbound firewall to your IPs.
- Ensure IB Client Portal Gateway is accessible from the backend service.
- Monitor logs and ensure Client Portal Gateway auto-restarts during maintenance windows.

## Notes
- This service proxies requests to the IB Client Portal Gateway.
- Time values are returned in ISO-8601 (UTC) where possible.

## License
Internal BSD project component. Consult project lead before distribution.
