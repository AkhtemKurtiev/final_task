from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.utils.auth_protect import admin_required
from src.database.db import get_async_session
from src.exceptions.exceptions import (
    CustomHTTPException,
    DepartmentNotFoundException,
    ParentDepartmentNotFoundException,
    PositionNotFoundException,
    RootDepartmentNotFoundException,
    UserNotFoundException,
)
from src.models.department import Department
from src.models.user import User
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class StructureService(BaseService):
    base_repository: Department

    @transaction_mode
    async def create_department(
        self,
        name: str,
        parent_id,
        current_user,
    ):
        try:
            company_id = current_user.company_id

            parent = None
            if parent_id:
                parent = await self.uow.department.get_department(parent_id)
                if not parent or parent.company_id != company_id:
                    raise ParentDepartmentNotFoundException()
            else:
                parent = await self.uow.department.get_department_filter(
                    company_id, is_can_deleted=False
                )
                if not parent:
                    raise RootDepartmentNotFoundException()

            new_department = await self.uow.department.add_department(
                department_name=name, company_id=company_id, parent=parent
            )

            return new_department
        except ParentDepartmentNotFoundException as e:
            raise e
        except RootDepartmentNotFoundException as e:
            raise e
        except Exception:
            raise CustomHTTPException()

    @transaction_mode
    async def create_position(
        self,
        name: str,
        department_id: int,
        current_user
    ):
        try:
            department = (
                await self.uow.department.get_department(department_id)
            )
            if not department:
                raise DepartmentNotFoundException()

            new_position = (
                await self.uow.position.add_position(name, department)
            )

            return new_position
        except DepartmentNotFoundException as e:
            raise e
        except Exception:
            raise CustomHTTPException()

    @transaction_mode
    async def assign_position_to_user(
        self,
        user_id: int,
        position_id: int,
        current_user: User = Depends(admin_required),
        db: AsyncSession = Depends(get_async_session)
    ):
        try:
            user = await self.uow.user.get_user_by_filter_id(user_id)
            if not user:
                raise UserNotFoundException()

            position = await self.uow.position.get_position(position_id)
            if not position:
                raise PositionNotFoundException()

            user.position = position
            await self.uow.user.update_user(user)

            return {'message': 'Position assigned to user successfully'}
        except UserNotFoundException as e:
            raise e
        except PositionNotFoundException as e:
            raise e
        except Exception:
            raise CustomHTTPException()

    @transaction_mode
    async def assign_manager(
        self,
        department_id: int,
        user_id: int,
        current_user
    ):
        try:
            department = (
                await self.uow.department.get_department(department_id)
            )
            if not department:
                raise DepartmentNotFoundException()

            user = await self.uow.user.get_user_by_filter_id(user_id)
            if not user:
                raise UserNotFoundException()

            department.manager_id = user.id
            await self.uow.department.update_department(department)

            return {
                'message': 'Manager assigned successfully',
                'department': department.name,
                'manager': user.first_name + ' ' + user.last_name
            }
        except DepartmentNotFoundException as e:
            raise e
        except UserNotFoundException as e:
            raise e
        except Exception:
            raise CustomHTTPException()

    @transaction_mode
    async def delete_department(
        self,
        department_id: int,
        current_user: User = Depends(admin_required)
    ):
        try:
            department = (
                await self.uow.department.get_department(department_id)
            )
            if not department:
                raise DepartmentNotFoundException()

            await self.uow.department.delete_department(department)

            return {'message': 'Department deleted successfully'}
        except DepartmentNotFoundException as e:
            raise e
        except Exception:
            raise CustomHTTPException()
