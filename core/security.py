import jwt
from datetime import datetime, timedelta, timezone
from core.config import settings

def create_access_token(
    subject: str,
    expires_delta_minutes: int = 60*24*15
) -> str:
    """
    Create an access token for a given subject (usually username or email)

    subject: This is usually the user's email or username - something unique to identify them
    expires_delta_minutes: Token expiry time (default: 15 days). You can adjust this based on your security needs
    exp: Expiration timestamp in UTC (JWT standard)
    """

    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta_minutes)
    to_encode = {
        "exp": expire, "sub": str(subject)
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt
