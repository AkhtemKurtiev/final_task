from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from src.models.task import TaskStatus


class TaskBase(BaseModel):
    title: str
    description: Optional[str]
    deadline: Optional[datetime]
    status: TaskStatus


class TaskCreate(TaskBase):
    author_id: int
    responsible_id: int


class RaskUpdate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int
    author_id: int
    response_id: int

    class Config:
        from_attributes = True
