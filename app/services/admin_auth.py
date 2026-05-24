"""JWT-based admin authentication.

A single admin user is configured via environment variables:
- ADMIN_USERNAME
- ADMIN_PASSWORD

On successful POST /v1/admin/auth/login we issue a signed JWT (HS256) using
ADMIN_JWT_SECRET. All other admin endpoints accept the token via
`Authorization: Bearer <token>`.
"""

import hmac
import time
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings


bearer_scheme = HTTPBearer(auto_error=False)


def verify_credentials(username: str, password: str) -> bool:
    """Constant-time comparison so we don't leak length via timing."""
    return (
        hmac.compare_digest(username or "", settings.ADMIN_USERNAME)
        and hmac.compare_digest(password or "", settings.ADMIN_PASSWORD)
    )


def issue_token(username: str) -> dict:
    now = int(time.time())
    exp_seconds = max(1, int(settings.ADMIN_JWT_EXP_HOURS)) * 3600
    payload = {
        "sub": username,
        "role": "admin",
        "iat": now,
        "exp": now + exp_seconds,
    }
    token = jwt.encode(payload, settings.ADMIN_JWT_SECRET, algorithm="HS256")
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": exp_seconds,
        "username": username,
    }


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.ADMIN_JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="TOKEN_EXPIRED",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="INVALID_TOKEN",
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_admin(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> str:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="MISSING_TOKEN",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_token(credentials.credentials)
    if payload.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="NOT_ADMIN",
        )
    return payload.get("sub", "")
