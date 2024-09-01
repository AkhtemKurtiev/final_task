from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.database.db import BaseModel


class InviteToken(BaseModel):
    __tablename__ = 'invite_tokens'

    id = Column(Integer, primary_key=True)
    token = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', back_populates='invite_tokens')
