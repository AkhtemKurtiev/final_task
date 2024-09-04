from src.api.user.v1.utils.email_message import (
    create_invite_token, send_invite_email, validate_invite_token
)
from src.auth.utils import encode_jwt, hash_password, validate_password
from src.exceptions.exceptions import (
    AccountAlreadyExistsException,
    BadTokenException,
    CustomHTTPException,
    EmailAlreadyRegisteredException,
    InvalidDataException,
    InvalidInviteTokenException,
    UserNotFoundException
)
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
                raise InvalidDataException()

            if not validate_password(user.password, db_user.hashed_password):
                raise InvalidDataException()
            access_token = encode_jwt({'sub': db_user.email})
            return {'access_token': access_token, 'token_type': 'bearer'}
        except InvalidDataException as e:
            raise e
        except Exception:
            raise CustomHTTPException()

    @transaction_mode
    async def check_account(
        self,
        email: str,
    ):
        try:
            db_user = await self.uow.user.get_user_by_filter_email(email)

            if db_user:
                raise EmailAlreadyRegisteredException()

            invite_token = create_invite_token(email)
            # await send_invite_email(email, invite_token)
            return {
                'masssege': 'Invite sent to email',
                'invite_token': invite_token
            }
        except EmailAlreadyRegisteredException as e:
            raise e
        except Exception:
            raise CustomHTTPException()

    @transaction_mode
    async def sign_up(
        self,
        data
    ):
        try:
            if not validate_invite_token(data.account, data.invite_token):
                raise InvalidInviteTokenException()
            return {"message": "Invite token validated"}
        except InvalidInviteTokenException as e:
            raise e
        except Exception:
            raise CustomHTTPException()

    @transaction_mode
    async def sign_up_complete(
        self,
        user
    ):
        try:
            db_user = await self.uow.user.get_user_by_filter_email(user.email)

            if db_user:
                raise AccountAlreadyExistsException()

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
        except AccountAlreadyExistsException as e:
            raise e
        except Exception:
            raise CustomHTTPException()

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
                raise EmailAlreadyRegisteredException()

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
        except EmailAlreadyRegisteredException as e:
            raise e
        except Exception:
            raise CustomHTTPException()

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
                raise BadTokenException()

            user = await self.uow.user.get_user_by_filter_id(
                invite_token.user_id
            )

            if not user:
                raise UserNotFoundException()

            hashed_password = hash_password(password)
            user.hashed_password = hashed_password
            user.is_active = True

            await self.uow.user.update_user(user)

            await self.uow.invite_token.delete_invite_token(invite_token)

            return {'massage': 'Registration completed successfully'}
        except BadTokenException as e:
            raise e
        except UserNotFoundException as e:
            raise e
        except Exception:
            raise CustomHTTPException()

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
                raise InvalidInviteTokenException()

            db_user = await self.uow.user.get_user_by_filter_email(new_email)

            if db_user:
                raise EmailAlreadyRegisteredException()

            current_user.email = new_email
            await self.uow.user.update_user(current_user)

            return {'message': 'Email updated successfully'}
        except InvalidInviteTokenException as e:
            raise e
        except EmailAlreadyRegisteredException as e:
            raise e
        except Exception:
            raise CustomHTTPException()

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
        except Exception:
            raise CustomHTTPException()
