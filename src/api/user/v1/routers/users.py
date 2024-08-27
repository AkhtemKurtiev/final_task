from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.shemas.user import (
    UserLogin,
    UserResgister,
    UserAdminCreateEmployee,
    UserName
)
from src.models.user import User
from src.models.invite_token import InviteToken
from src.models.company import Company
from src.auth.utils import hash_password, validate_password, encode_jwt
from src.database.db import get_async_session
from src.api.user.v1.utils.email_message import (
    create_invite_token, send_invite_email, validate_invite_token
)
from src.api.user.v1.utils.auth_protect import (
    admin_required, authorized_user_required
)

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


oauth2_sheme = OAuth2PasswordBearer(tokenUrl='/login')


@router.post('/login')
async def login(
    user: dict = Depends(UserLogin),
    db: AsyncSession = Depends(get_async_session)
):
    result = await db.execute(select(User).filter(User.email == user.email))
    db_user = result.scalars().first()
    if not db_user:
        raise HTTPException(status_code=400, detail='Invalid data')

    if not validate_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail='Invalid data')

    access_token = encode_jwt({'sub': db_user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/check_account/{email}')
async def check_account(
    email: str,
    db: AsyncSession = Depends(get_async_session)
):
    result = await db.execute(select(User).filter(User.email == email))
    db_user = result.scalars().first()

    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')

    invite_token = create_invite_token(email)
    await send_invite_email(email, invite_token)
    return {'masssege': 'Invite sent to email', 'invite_token': invite_token}


@router.post('/sign-up/')
async def sign_up(
    account: str,
    invite_token: str,
    db: AsyncSession = Depends(get_async_session)
):
    if not validate_invite_token(account, invite_token):
        raise HTTPException(status_code=400, detail='Invalid invite token')
    return {"message": "Invite token validated"}


@router.post('/sign-up-complete/')
async def sign_up_complete(
    user: dict = Depends(UserResgister),
    db: AsyncSession = Depends(get_async_session)
):
    result = await db.execute(select(User).filter(User.email == user.email))
    db_user = result.scalars().first()

    if db_user:
        raise HTTPException(status_code=400, detail='Account already exists')

    new_company = Company(name=user.company_name)
    db.add(new_company)
    await db.commit()
    await db.refresh(new_company)

    hashed_password = hash_password(user.password)
    new_user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        hashed_password=hashed_password,
        company_id=new_company.id,
        is_admin=True
    )
    db.add(new_user)
    await db.commit()
    return {"message": "Registration complete. Admin user created."}


@router.post('/create-employee/')
async def create_employee(
    employee: dict = Depends(UserAdminCreateEmployee),
    current_user: User = Depends(admin_required),
    db: AsyncSession = Depends(get_async_session)
):
    result = await db.execute(
        select(User).filter(User.email == employee.email)
    )
    db_user = result.scalars().first()

    if db_user:
        raise HTTPException(
            status_code=400, detail="User with this email already exists"
        )

    new_employee = User(
        email=employee.email,
        first_name=employee.first_name,
        last_name=employee.last_name,
        username=employee.username,
        company_id=current_user.company_id,
        is_admin=False,
        is_active=False
    )

    db.add(new_employee)
    await db.commit()
    await db.refresh(new_employee)

    invite_token = create_invite_token(employee.email)

    invite = InviteToken(
        token=invite_token,
        user_id=new_employee.id
    )

    db.add(invite)
    await db.commit()

    await send_invite_email(employee.email, invite_token)
    return {'messege': 'Employee created and invite sent to email'}


@router.post('/confirm-registration-employee/')
async def confirm_registration(
    token: str,
    password: str,
    db: AsyncSession = Depends(get_async_session)
):
    result = await db.execute(
        select(InviteToken).filter(InviteToken.token == token)
    )
    invite_token = result.scalars().first()

    if not invite_token:
        raise HTTPException(status_code=400, detail='Bad token')

    result = await db.execute(
        select(User).filter(User.id == invite_token.user_id)
    )
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=400, detail='User not found')

    hashed_password = hash_password(password)
    user.hashed_password = hashed_password
    user.is_active = True

    db.add(user)
    await db.commit()

    await db.delete(invite_token)
    await db.commit()

    return {'massage': 'Registration completed successfully'}


@router.post('/email_update/')
async def email_update(
    token: str,
    new_email: str,
    current_user: User = Depends(authorized_user_required),
    db: AsyncSession = Depends(get_async_session)
):
    if not validate_invite_token(new_email, token):
        raise HTTPException(status_code=400, detail='Invalid invite token')

    result = await db.execute(select(User).filter(User.email == new_email))
    db_user = result.scalars().first()

    if db_user:
        raise HTTPException(status_code=400, detail='Email is already use')

    current_user.email = new_email
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)

    return {'message': 'Email updated successfully'}


@router.post('/name_update/')
async def name_update(
    name: dict = Depends(UserName),
    current_user: User = Depends(authorized_user_required),
    db: AsyncSession = Depends(get_async_session)
):
    current_user.first_name = name.first_name
    current_user.last_name = name.last_name

    db.add(current_user)
    await db.commit()
    db.refresh(current_user)

    return {'message': 'Name update successfully'}
