from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPBearer, OAuth2PasswordBearer, HTTPAuthorizationCredentials
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.user import User
from src.database.db import get_async_session
from src.auth.utils import decode_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

http_bearer = HTTPBearer()


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: AsyncSession = Depends(get_async_session)
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Not validate',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        token = credentials.credentials
        payload = decode_jwt(token)
        email: str = payload.get('sub')
        if email is None:
            raise credential_exception
    except Exception:
        raise credential_exception

    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalars().first()
    if user is None:
        raise credential_exception
    return user


def authorized_user_required(current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Authorization required (user)',
        )
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Authorization required (user.active)',
        )
    return current_user


def admin_required(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin or not current_user.is_active:
        if not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Authorization required (Admin.admin)',
            )
    return current_user
