from src.exceptions.exceptions import (
    CustomHTTPException,
    TaskNotFoundException
)
from src.models.task import Task
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class TaskService(BaseService):
    base_repository: Task

    @transaction_mode
    async def task_create(
        self,
        task_data,
        current_user,
    ):
        try:
            observers = [
                        await self.uow.user.get_user_by_filter_id(user_id)
                        for user_id in task_data.observers
                ]
            performers = [
                        await self.uow.user.get_user_by_filter_id(user_id)
                        for user_id in task_data.performers
                ]
            task_data.observers = observers
            task_data.performers = performers

            await self.uow.task.add_task(task_data, current_user)

            return {'message': 'Task create.'}
        except Exception:
            raise CustomHTTPException()

    @transaction_mode
    async def task_update(
        self,
        task_id: int,
        task_update,
        current_user,
    ):
        try:
            task = (
                await self.uow.task.get_task_by_filter_id_load_connected_objects(
                    task_id
                )
            )
            if not task:
                raise TaskNotFoundException()

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
                    observer = (
                        await self.uow.user.get_user_by_filter_id(observer_id)
                    )
                    if observer:
                        task.observers.append(observer)

            if task_update.performers is not None:
                task.performers.clear()
                for performer_id in task_update.performers:
                    performer = (
                        await self.uow.user.get_user_by_filter_id(performer_id)
                    )
                    if performer:
                        task.performers.append(performer)

            await self.uow.task.update_task(task)

            return {'message': 'Task updated.'}
        except TaskNotFoundException as e:
            raise e
        except Exception:
            raise CustomHTTPException()

    @transaction_mode
    async def task_delete(
        self,
        task_id: int,
        current_user,
    ):
        try:
            task = await self.uow.task.get_task_by_filter_id(task_id)
            if not task:
                raise TaskNotFoundException()

            await self.uow.task.delete_task(task)

            return {'message': 'Task delete.'}
        except TaskNotFoundException as e:
            raise e
        except Exception:
            raise CustomHTTPException()
