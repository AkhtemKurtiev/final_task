import enum

from sqlalchemy import (
    Column, String, Integer, ForeignKey, DateTime, Enum, Text
)
from sqlalchemy.orm import relationship

from src.database.db import BaseModel


class TaskStatus(enum.Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'


class Task(BaseModel):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    author_id = Column(Integer, ForeignKey('user.id'))
    responsible_id = Column(Integer, ForeignKey('user.id'))
    deadline = Column(DateTime, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)

    author = relationship(
        'User',
        foreign_keys=[author_id],
        back_populates='authored_tasks'
    )
    responsible = relationship(
        'User',
        foreign_keys=[responsible_id],
        back_populates='responsible_tasks'
    )
