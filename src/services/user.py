from fastapi import HTTPException

from src.api.user.v1.utils.email_message import (
    create_invite_token, send_invite_email, validate_invite_token
)
from src.auth.utils import encode_jwt, hash_password, validate_password
from src.models.user import User
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class UserService(BaseService):
    base_repository: User

    @transaction_mode
    async def login(
        self,
        user,
    ):
        try:
            db_user = await self.uow.user.get_user_by_filter_email(user.email)
            if not db_user:
                raise HTTPException(status_code=400, detail='Invalid data1')

            if not validate_password(user.password, db_user.hashed_password):
                raise HTTPException(status_code=400, detail='Invalid data2')

            access_token = encode_jwt({'sub': db_user.email})
            return {'access_token': access_token, 'token_type': 'bearer'}
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail={
                'status': 'error',
                'data': None,
                'detail': None
                })

    @transaction_mode
    async def check_account(
        self,
        email: str,
    ):
        try:
            db_user = await self.uow.user.get_user_by_filter_email(email)

            if db_user:
                raise HTTPException(
                    status_code=400,
                    detail='Email already registered'
                )

            invite_token = create_invite_token(email)
            # await send_invite_email(email, invite_token)
            return {
                'masssege': 'Invite sent to email',
                'invite_token': invite_token
            }
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail={
                'status': 'error',
                'data': None,
                'detail': None
                })

    @transaction_mode
    async def sign_up(
        self,
        account: str,
        invite_token: str
    ):
        try:
            if not validate_invite_token(account, invite_token):
                raise HTTPException(
                    status_code=400,
                    detail='Invalid invite token'
                )
            return {"message": "Invite token validated"}
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail={
                'status': 'error',
                'data': None,
                'detail': None
                })

    @transaction_mode
    async def sign_up_complete(
        self,
        user
    ):
        try:
            db_user = await self.uow.user.get_user_by_filter_email(user.email)

            if db_user:
                raise HTTPException(
                    status_code=400,
                    detail='Account already exists'
                )

            new_company = await self.uow.company.add_company(user.company_name)

            hashed_password = hash_password(user.password)

            await self.uow.user.add_user(user, hashed_password, new_company.id)

            department_name = f'Department {new_company.name}'

            await self.uow.department.add_department(
                department_name,
                new_company.id,
                parent=None,
                is_can_deleted=False
            )

            return {"message": "Registration complete. Admin user created."}
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail={
                'status': 'error',
                'data': None,
                'detail': None
                })

    @transaction_mode
    async def create_employee(
        self,
        employee,
        current_user
    ):
        try:
            db_user = (
                await self.uow.user.get_user_by_filter_email(employee.email)
            )

            if db_user:
                raise HTTPException(
                    status_code=400,
                    detail="User with this email already exists"
                )

            new_employee = await self.uow.user.add_user_first_step(
                employee,
                current_user.company_id
            )

            invite_token = create_invite_token(employee.email)

            await self.uow.invite_token.add_invite_token(
                invite_token,
                new_employee.id
            )

            # await send_invite_email(employee.email, invite_token)
            return {'messege': 'Employee created and invite sent to email'}
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail={
                'status': 'error',
                'data': None,
                'detail': None
                })

    @transaction_mode
    async def confirm_registration(
        self,
        token: str,
        password: str
    ):
        try:
            invite_token = (
                await self.uow.invite_token.get_invite_token_filter(token)
            )

            if not invite_token:
                raise HTTPException(status_code=400, detail='Bad token')

            user = await self.uow.user.get_user_by_filter_id(
                invite_token.user_id
            )

            if not user:
                raise HTTPException(status_code=400, detail='User not found')

            hashed_password = hash_password(password)
            user.hashed_password = hashed_password
            user.is_active = True

            await self.uow.user.update_user(user)

            await self.uow.invite_token.delete_invite_token(invite_token)

            return {'massage': 'Registration completed successfully'}
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail={
                'status': 'error',
                'data': None,
                'detail': None
                })

    @transaction_mode
    async def email_update(
        self,
        token,
        new_email,
        current_user,
    ):
        try:
            current_user = (
                await self.uow.user.get_user_by_filter_id(current_user.id)
            )
            if not validate_invite_token(new_email, token):
                raise HTTPException(
                    status_code=400, detail='Invalid invite token'
                )

            db_user = await self.uow.user.get_user_by_filter_email(new_email)

            if db_user:
                raise HTTPException(
                    status_code=400, detail='Email is already use'
                )

            current_user.email = new_email
            await self.uow.user.update_user(current_user)

            return {'message': 'Email updated successfully'}
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail={
                'status': 'error',
                'data': None,
                'detail': None
                })

    @transaction_mode
    async def name_update(
        self,
        name,
        current_user
    ):
        try:
            current_user = (
                await self.uow.user.get_user_by_filter_id(current_user.id)
            )
            current_user.first_name = name.first_name
            current_user.last_name = name.last_name

            await self.uow.user.update_user(current_user)

            return {'message': 'Name update successfully'}
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail={
                'status': 'error',
                'data': None,
                'detail': None
                })
