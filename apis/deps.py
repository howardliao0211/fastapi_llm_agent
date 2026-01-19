import jwt
from sqlmodel import Session, select
from database.db import engine
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.config import settings
from database.models.user import User

def get_db():
    with Session(engine) as session:
        yield session

"""
This line of code tells FastAPI if anyone needs to get a token,
send them to /api/v1/token
"""
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/token")

def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session=Depends(get_db)
) -> User:
    """
    We use oauth2_scheme to automatically extract token from the request headers. 
    """
    
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate user credential",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credential_exception
    except jwt.InvalidTokenError:
        raise credential_exception

    statement = select(User).where(User.email == email)
    result = db.exec(statement)
    user = result.first()
    if user is None:
        raise credential_exception
    return user
