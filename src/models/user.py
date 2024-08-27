from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, String, LargeBinary
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import BaseModel


class User(BaseModel):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(32), unique=True)
    hashed_password = Column(LargeBinary, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    company_id = Column(Integer, ForeignKey('companies.id'), nullable=True)
    position_id = Column(Integer, ForeignKey('positions.id'), nullable=True)

    company = relationship('Company', back_populates='employees')
    position = relationship('Position', back_populates='users')
    authored_tasks = relationship(
        'Task',
        foreign_keys='Task.author_id',
        back_populates='author'
    )
    responsible_tasks = relationship(
        'Task',
        foreign_keys='Task.responsible_id',
        back_populates='responsible'
    )

    invite_tokens = relationship(
        'InviteToken',
        back_populates='user'
    )
