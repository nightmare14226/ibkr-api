from __future__ import annotations

import secrets
import time
from threading import Lock
from typing import Dict


class TokenStore:
    """
    Simple in-memory bearer token store with expiration.
    Intended for lightweight scenarios (single process).
    """

    def __init__(self, ttl_seconds: int = 60 * 60) -> None:
        self.ttl = ttl_seconds
        self._tokens: Dict[str, float] = {}
        self._lock = Lock()

    def _cleanup(self) -> None:
        now = time.time()
        expired = [token for token, expiry in self._tokens.items() if expiry <= now]
        for token in expired:
            self._tokens.pop(token, None)

    def issue(self) -> str:
        token = secrets.token_urlsafe(32)
        expires_at = time.time() + self.ttl
        with self._lock:
            self._cleanup()
            self._tokens[token] = expires_at
        return token

    def is_valid(self, token: str) -> bool:
        with self._lock:
            self._cleanup()
            expiry = self._tokens.get(token)
            if expiry is None:
                return False
            if expiry <= time.time():
                self._tokens.pop(token, None)
                return False
            return True

    def revoke(self, token: str) -> None:
        with self._lock:
            self._tokens.pop(token, None)


# Default singleton used by the app
token_store = TokenStore()

