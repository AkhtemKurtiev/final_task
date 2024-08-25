from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database.db import BaseModel


class Position(BaseModel):
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True)
    name = Column(String,  unique=True, nullable=False)

    users = relationship('User', back_populates='position')
