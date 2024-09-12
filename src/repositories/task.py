from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.models.task import Task
from src.utils.repository import SqlAlchemyRepository


class TaskRepository(SqlAlchemyRepository):
    model = Task

    async def add_task(self, task, current_user):
        new = self.model(
            title=task.title,
            description=task.description,
            author_id=current_user.id,
            responsible_id=task.responsible_id,
            deadline=task.deadline,
            status=task.status,
            observers=task.observers,
            performers=task.performers
        )
        self.session.add(new)
        return new

    async def get_task_by_filter_id(self, task_id):
        result = await self.session.execute(select(self.model).filter(self.model.id == task_id))
        return result.scalars().first()

    async def get_task_by_filter_id_load_connected_objects(self, id):
        result = await self.session.execute(
            select(self.model).options(
                selectinload(self.model.observers),
                selectinload(self.model.performers)
            ).filter(Task.id == id)
        )
        return result.scalars().first()

    async def update_task(self, task):
        self.session.add(task)

    async def delete_task(self, task):
        await self.session.delete(task)
