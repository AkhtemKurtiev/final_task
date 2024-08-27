from sqlalchemy import Column, Integer, String,  ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from src.database.db import BaseModel


class Position(BaseModel):
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))

    users = relationship('User', back_populates='position')
    department = relationship('Department', back_populates='positions')

    __table_args__ = (
        UniqueConstraint('name', 'department_id', name='_name_department_'),
    )
