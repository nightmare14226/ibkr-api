# BSD IBKR Gateway (FastAPI)

A lightweight API to connect to Interactive Brokers (IBKR) and expose REST endpoints that Power BI can refresh on demand.

## Features
- Secure endpoints (API key header)
- Endpoints: health, symbols search, quotes, historical bars, positions, account PnL
- JSON outputs friendly for Power BI ingestion
- Designed for self-hosting on VPS/Azure

## Prerequisites
- Python 3.11+
- Interactive Brokers TWS or IB Gateway running and configured to accept API connections
  - Host: typically `127.0.0.1`
  - Port: Paper `7497`, Live `7496` (or custom)
  - Set a fixed `Client ID` in both TWS/Gateway and this service
- Market data subscriptions for requested instruments

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

Add header `X-API-Key: <your_api_key>` for protected endpoints.

## Environment variables (.env)
```
API_KEY=change-me
IB_HOST=127.0.0.1
IB_PORT=7497
IB_CLIENT_ID=123
ALLOWED_ORIGINS=*
TIMEZONE=UTC
```

## Example endpoints
- `GET /health` (no auth)
- `GET /api/v1/symbols?query=AAPL`
- `GET /api/v1/quotes?symbol=AAPL&exchange=SMART&currency=USD`
- `GET /api/v1/history?symbol=AAPL&duration=1%20D&barSize=1%20min&whatToShow=TRADES&useRTH=true`
- `GET /api/v1/positions`
- `GET /api/v1/pnl` (optional `account`)

All `/api/v1/*` endpoints require `X-API-Key` header.

## Power BI setup (Desktop)
1. In Power BI Desktop, use `Get Data` -> `Web`.
2. Enter endpoint URL (e.g., `http://<server>:8000/api/v1/history?symbol=AAPL&duration=1%20M&barSize=1%20day`).
3. In `Advanced`, add HTTP request header: `X-API-Key` with your API key.
4. Transform to table, expand records as needed.
5. Parameterize `symbol`, `duration`, `barSize` and enable incremental refresh for historical tables.

## Production deployment (VPS/Azure)
- Use a process manager (e.g., `systemd`) to run `uvicorn app.main:app --host 0.0.0.0 --port 8000`.
- Put NGINX/Caddy in front for HTTPS termination.
- Restrict inbound firewall to your IPs, and require API key (`X-API-Key`).
- Monitor logs and set TWS/IB Gateway to auto-restart daily maintenance windows.

## Notes
- IBKR has pacing limits. The service performs basic retries and caching is recommended for heavy usage.
- Time values are returned in ISO-8601 (UTC) where possible.

## License
Internal BSD project component. Consult project lead before distribution.
