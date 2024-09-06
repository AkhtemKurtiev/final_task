from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.api.utils.auth_protect import authorized_user_required
from src.models.user import User
from src.services.task import TaskService
from src.shemas.task import TaskCreate, TaskUpdate
from src.shemas.task_router import MessageResponse


router = APIRouter(
    prefix='/task',
    tags=['Task']
)


@router.post('/task_create/', status_code=HTTP_201_CREATED)
async def task_create(
    task_data: dict = Depends(TaskCreate),
    current_user: User = Depends(authorized_user_required),
    service: TaskService = Depends(TaskService)
) -> MessageResponse:
    return await service.task_create(task_data, current_user)


@router.put('/task_update/{task_id}/', status_code=HTTP_200_OK)
async def task_update(
    task_id: int,
    task_update: dict = Depends(TaskUpdate),
    current_user: User = Depends(authorized_user_required),
    service: TaskService = Depends(TaskService)
) -> MessageResponse:
    return await service.task_update(task_id, task_update, current_user)


@router.delete('/task_delete/{task_id}/', status_code=HTTP_204_NO_CONTENT)
async def task_delete(
    task_id: int,
    current_user: User = Depends(authorized_user_required),
    service: TaskService = Depends(TaskService)
) -> MessageResponse:
    return await service.task_delete(task_id, current_user)
