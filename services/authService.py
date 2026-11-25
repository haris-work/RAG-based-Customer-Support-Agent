
import os
import secrets

from pathlib import Path

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


admin_key_header = APIKeyHeader(
    name="X-Admin-Key",
    auto_error=False
)


def VerifyAdminKey(
    provided_key: str | None = Depends(admin_key_header)
):

    expected_key = os.getenv("ADMIN_API_KEY")

    if not expected_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Admin authentication is not configured"
        )

    if (
        not provided_key
        or not secrets.compare_digest(
            provided_key,
            expected_key
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing administrator API key"
        )

    return True
