from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from ..core.security import token_store


class BearerAuthMiddleware(BaseHTTPMiddleware):
    """Ensure POST requests include a valid Bearer token."""

    def __init__(self, app, excluded_paths: set[str] | None = None) -> None:
        super().__init__(app)
        self.excluded_paths = excluded_paths or set()

    async def dispatch(self, request: Request, call_next):
        if request.method.upper() == "POST":
            if request.url.path not in self.excluded_paths:
                auth_header = request.headers.get("Authorization")
                if not auth_header or not auth_header.startswith("Bearer "):
                    return JSONResponse(
                        status_code=401,
                        content={"detail": "Missing or invalid Authorization header"},
                    )
                token = auth_header.split(" ", 1)[1].strip()
                if not token_store.is_valid(token):
                    return JSONResponse(
                        status_code=401,
                        content={"detail": "Invalid or expired token"},
                    )
        return await call_next(request)

