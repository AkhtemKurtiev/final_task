from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.shemas.user import UserCreate, UserResponseRegister, UserLogin
from src.models.user import User
from src.auth.utils import hash_password, validate_password, encode_jwt
from src.database.db import get_async_session

router = APIRouter(
    prefix='/users',
    tags=['User']
)


@router.post('/register/', response_model=UserResponseRegister)
async def register(user: dict = Depends(UserCreate), db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(User).filter(User.email == user.email))
    db_user = result.scalars().first()
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')

    hashed_password = hash_password(user.password)

    new_user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        hashed_password=hashed_password,
        company_id=user.company_id,
        position_id=user.position_id
    )
    db.add(new_user)
    await db.commit()
    return new_user


@router.post('/login')
async def login(user: dict = Depends(UserLogin), db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(User).filter(User.email == user.email))
    db_user = result.scalars().first()
    if not db_user:
        raise HTTPException(status_code=400, detail='Invalid data')

    if not validate_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail='Invalid data')

    access_token = encode_jwt({'sub': db_user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}
