from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.settings import settings
from src.db.db_models import User
from src.db.session import get_session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.secret, algorithm=settings.algorithm)
    return encoded_jwt


def get_id_from_access_token(token: str, credentials_exception) -> int:
    try:
        payload = jwt.decode(token, settings.secret, [settings.algorithm])
        idx = payload.get("user_id")

        if idx is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    return idx


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_session)
) -> int:
    """Verifys user's access token, checks if user in db and returns user_id."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_id = get_id_from_access_token(token, credentials_exception)

    query = select(User).where(User.id == user_id)
    res = await db.execute(query)
    user = res.scalars().first()
    if not user:
        raise credentials_exception

    return user_id
