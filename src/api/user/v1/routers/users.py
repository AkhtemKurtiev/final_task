from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from src.api.utils.auth_protect import (
    admin_required, authorized_user_required
)
from src.models.user import User
from src.services.user import UserService
from src.shemas.user import (
    UserAdminCreateEmployee,
    UserLogin,
    UserName,
    UserSignUp,
    UserRegister
)


router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


oauth2_sheme = OAuth2PasswordBearer(tokenUrl='/login')


@router.post('/login')
async def login(
    user: dict = Depends(UserLogin),
    service: UserService = Depends(UserService)
):
    return await service.login(user)


@router.get('/check_account/{email}')
async def check_account(
    email: str,
    service: UserService = Depends(UserService)
):
    return await service.check_account(email)


@router.post('/sign-up/')
async def sign_up(
    data: dict = Depends(UserSignUp),
    service: UserService = Depends(UserService)
):
    return await service.sign_up(data)


@router.post('/sign-up-complete/')
async def sign_up_complete(
    user: dict = Depends(UserRegister),
    service: UserService = Depends(UserService)
):
    return await service.sign_up_complete(user)


@router.post('/create-employee/')
async def create_employee(
    employee: dict = Depends(UserAdminCreateEmployee),
    current_user: User = Depends(admin_required),
    service: UserService = Depends(UserService)
):
    return await service.create_employee(employee, current_user)


@router.post('/confirm-registration-employee/')
async def confirm_registration(
    token: str,
    password: str,
    service: UserService = Depends(UserService)
):
    return await service.confirm_registration(token, password)


@router.put('/email_update/')
async def email_update(
    token: str,
    new_email: str,
    current_user: User = Depends(authorized_user_required),
    service: UserService = Depends(UserService)
):
    return await service.email_update(token, new_email, current_user)


@router.put('/name_update/')
async def name_update(
    name: dict = Depends(UserName),
    current_user: User = Depends(authorized_user_required),
    service: UserService = Depends(UserService)
):
    return await service.name_update(name, current_user)
