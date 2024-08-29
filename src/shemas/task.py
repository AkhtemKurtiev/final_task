from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from src.models.task import TaskStatus


class TaskBase(BaseModel):
    title: str
    description: Optional[str]
    deadline: Optional[datetime]
    status: TaskStatus


class TaskResponse(TaskBase):
    id: int
    author_id: int
    response_id: int

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    responsible_id: int
    deadline: Optional[datetime] = '2030-08-29'
    status: TaskStatus = TaskStatus.PENDING
    observers: Optional[List[int]] = Field(default_factory=list)
    performers: Optional[List[int]] = Field(default_factory=list)

    class Config:
        orm_mode = True


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    responsible_id: Optional[int] = None
    deadline: Optional[datetime] = None
    status: Optional[TaskStatus] = None
    observers: Optional[List[int]] = Field(default_factory=list)
    performers: Optional[List[int]] = Field(default_factory=list)

    class Config:
        orm_mode = True
