import os
from pydantic import BaseModel


class Settings(BaseModel):
    # Interactive Brokers connection
    ib_host: str = os.getenv("IB_HOST", "127.0.0.1")
    ib_port: int = int(os.getenv("IB_PORT", "7497"))  # Paper: 7497, Live: 7496 (default)
    ib_client_id: int = int(os.getenv("IB_CLIENT_ID", "123"))

    # API security
    api_key: str = os.getenv("API_KEY", "change-me")

    # CORS
    allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "*")

    # General
    timezone: str = os.getenv("TIMEZONE", "UTC")


settings = Settings()

