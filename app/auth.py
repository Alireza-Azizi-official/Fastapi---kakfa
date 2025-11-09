from datetime import datetime, timedelta, timezone

from jose import jwt

from app.config import settings


def create_jwt(username: str):
    payload = {
        "sub": username,
        "exp": datetime.now(tz=timezone.utc) + timedelta(hours=2),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def verify_jwt(token: str):
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload.get("sub")
    except Exception:
        return None
