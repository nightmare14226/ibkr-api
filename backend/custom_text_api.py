from fastapi import FastAPI, HTTPException
import requests

app = FastAPI(title="Custom API")
IBKR_BASE_URL = "https://localhost:5000/v1/api"
VERIFY_SSL = False

@app.get("/")
def root():
    return {"message": "IBKR custom API is running"}
    
@app.get("/ibkr/status")
def get_auth_status():
    """Check if IBKR gateway session is active"""
    try:
        response = requests.get(f"{IBKR_BASE_URL}/iserver/auth/status", verify=VERIFY_SSL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, delattr=str(e))

@app.get("/ibkr/account")
def get_account_summary():
    """Fetch account summary"""
    try:
        response = requests.get(f"{IBKR_BASE_URL}/iserver/account", verify=VERIFY_SSL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
        