import os
from pydantic import BaseModel


class Settings(BaseModel):
    # IB Client Portal Gateway URL
    ib_gateway_url: str = os.getenv("IB_GATEWAY_URL", "https://localhost:5000/v1/api")

    # CORS
    allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "*")

    # General
    timezone: str = os.getenv("TIMEZONE", "UTC")

    # API authentication
    api_username: str = os.getenv("API_USERNAME", "admin")
    api_password: str = os.getenv("API_PASSWORD", "changeme")

    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./ares.db")


settings = Settings()

