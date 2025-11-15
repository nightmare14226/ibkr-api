from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel

from ..config import settings
from ..core.security import token_store


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LogoutResponse(BaseModel):
    detail: str


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest):
    if payload.username != settings.api_username or payload.password != settings.api_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = token_store.issue()
    return LoginResponse(access_token=token)


@router.post("/logout", response_model=LogoutResponse)
async def logout(authorization: str = Header(..., alias="Authorization")):
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Authorization header")
    token = authorization.split(" ", 1)[1].strip()
    token_store.revoke(token)
    return LogoutResponse(detail="Logged out")

