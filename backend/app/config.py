import os
from pydantic import BaseModel


class Settings(BaseModel):
    # IB Client Portal Gateway URL
    ib_gateway_url: str = os.getenv("IB_GATEWAY_URL", "https://localhost:5000/v1/api")

    # CORS
    allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "*")

    # General
    timezone: str = os.getenv("TIMEZONE", "UTC")


settings = Settings()

