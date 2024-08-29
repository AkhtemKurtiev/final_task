from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from src.database.db import get_async_session
from src.models.department import Department
from src.models.position import Position
from src.models.user import User
from src.api.utils.auth_protect import admin_required

router = APIRouter(
    prefix='/structure',
    tags=['Structure']
)


@router.post('/departments/')
async def create_department(
    name: str,
    parent_id: Optional[int] = None,
    current_user: User = Depends(admin_required),
    db: AsyncSession = Depends(get_async_session)
):
    company_id = current_user.company_id

    parent = None
    if parent_id:
        parent = await db.get(Department, parent_id)

    new_department = Department(
        name=name,
        parent=parent,
        company_id=company_id
    )
    await new_department.initialize(db)
    db.add(new_department)
    await db.commit()

    return new_department


@router.post('/positions/')
async def create_position(
    name: str,
    department_id: int,
    current_user: User = Depends(admin_required),
    db: AsyncSession = Depends(get_async_session)
):
    department = await db.get(Department, department_id)
    if not department:
        raise HTTPException(status_code=404,  detail='Department not found')

    new_position = Position(name=name, department=department)
    db.add(new_position)
    await db.commit()
    await db.refresh(new_position)

    return new_position


@router.post('/assign-position/')
async def assign_position_to_user(
    user_id: int,
    position_id: int,
    current_user: User = Depends(admin_required),
    db: AsyncSession = Depends(get_async_session)
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    position = await db.get(Position, position_id)
    if not position:
        raise HTTPException(status_code=404, detail='Position not found')

    user.position = position
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {'message': 'Position assigned to user successfully'}


@router.post('/departments/{department_id}/assign-manager/')
async def assign_manager(
    department_id: int,
    user_id: int,
    current_user: User = Depends(admin_required),
    db: AsyncSession = Depends(get_async_session)
):
    department = await db.get(Department, department_id)
    if not department:
        raise HTTPException(status_code=404, detail='Department not found')

    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    department.manager_id = user.id
    db.add(department)
    await db.commit()
    await db.refresh(department)

    return {
        'message': 'Manager assigned successfully',
        'department': department.name,
        'manager': user.first_name + ' ' + user.last_name
    }


@router.delete('/departments/delete/')
async def delete_department(
    department_id: int,
    current_user: User = Depends(admin_required),
    db: AsyncSession = Depends(get_async_session)
):
    department = await db.get(Department, department_id)
    if not department:
        raise HTTPException(status_code=404, detail='Department not found')

    await department.delete_department(db)

    return {'message': 'Department deleted successfully'}
