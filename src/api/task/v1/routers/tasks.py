from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


from src.database.db import get_async_session
from src.models.department import Department
from src.models.position import Position
from src.models.user import User
from src.models.task import Task

from src.shemas.task import TaskCreate, TaskUpdate
from src.api.utils.auth_protect import admin_required, authorized_user_required


router = APIRouter(
    prefix='/task',
    tags=['Task']
)


@router.post('/task_create/')
async def task_create(
    task_data: dict = Depends(TaskCreate),
    current_user: User = Depends(authorized_user_required),
    db: AsyncSession = Depends(get_async_session)
):
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        author_id=current_user.id,
        responsible_id=task_data.responsible_id,
        deadline=task_data.deadline,
        status=task_data.status,
        observers=[
            await db.get(User, user_id) for user_id in task_data.observers
        ],
        performers=[
            await db.get(User, user_id) for user_id in task_data.performers
        ]
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return {'message': 'Task create.'}


@router.put('/task_update/{task_id}/')
async def task_update(
    task_id: int,
    task_update: dict = Depends(TaskUpdate),
    current_user: User = Depends(authorized_user_required),
    db: AsyncSession = Depends(get_async_session)
):
    result = await db.execute(
        select(Task)
        .options(selectinload(Task.observers), selectinload(Task.performers))
        .filter(Task.id == task_id)
    )
    task = result.scalars().first()

    if not task:
        raise HTTPException(status_code=404, detail='Task not found')

    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.responsible_id is not None:
        task.responsible_id = task_update.responsible_id
    if task_update.deadline is not None:
        task.deadline = task_update.deadline
    if task_update.status is not None:
        task.status = task_update.status

    if task_update.observers is not None:
        task.observers.clear()
        for observer_id in task_update.observers:
            observer = await db.get(User, observer_id)
            if observer:
                task.observers.append(observer)

    if task_update.performers is not None:
        task.performers.clear()
        for performer_id in task_update.performers:
            performer = await db.get(User, performer_id)
            if performer:
                task.performers.append(performer)

    db.add(task)
    await db.commit()
    await db.refresh(task)

    return {'message': 'Task updated.'}


@router.delete('/task_delete/{task_id}/')
async def task_delete(
    task_id: int,
    current_user: User = Depends(authorized_user_required),
    db: AsyncSession = Depends(get_async_session)
):
    result = await db.execute(select(Task).filter(Task.id == task_id))
    task = result.scalars().first()

    if not task:
        raise HTTPException(status_code=404, detail='Task not found')

    await db.delete(task)
    await db.commit()

    return {'message': 'Task delete.'}
