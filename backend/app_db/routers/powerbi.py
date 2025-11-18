import os
import msal  # pyright: ignore[reportMissingImports]
import httpx
from fastapi import APIRouter
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
WORKSPACE_ID = os.getenv("WORKSPACE_ID")
REPORT_ID = os.getenv("REPORT_ID")

# MSAL App for Azure AD
msal_app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=f"https://login.microsoftonline.com/{TENANT_ID}",
    client_credential=CLIENT_SECRET
)


def get_access_token():
    """Return Azure AD token for Power BI REST API."""
    result = msal_app.acquire_token_for_client(
        scopes=["https://analysis.windows.net/powerbi/api/.default"]
    )
    return result["access_token"]


@router.get("/api/get-embed-config")
async def get_powerbi_embed():
    """Return embedToken + embedUrl + reportId for frontend."""
    try:
        access_token = get_access_token()

        # 1️⃣ Get report metadata (embedUrl)
        async with httpx.AsyncClient() as client:
            report_res = await client.get(
                f"https://api.powerbi.com/v1.0/myorg/groups/{WORKSPACE_ID}/reports/{REPORT_ID}",
                headers={"Authorization": f"Bearer {access_token}"}
            )
        embed_url = report_res.json()["embedUrl"]

        # 2️⃣ Generate embed token
        async with httpx.AsyncClient() as client:
            token_res = await client.post(
                f"https://api.powerbi.com/v1.0/myorg/groups/{WORKSPACE_ID}/reports/{REPORT_ID}/GenerateToken",
                headers={"Authorization": f"Bearer {access_token}"},
                json={"accessLevel": "View"}
            )

        embed_token = token_res.json()["token"]

        # 3️⃣ Return to frontend
        return {
            "reportId": REPORT_ID,
            "embedUrl": embed_url,
            "embedToken": embed_token
        }

    except Exception as e:
        return {"error": str(e)}
