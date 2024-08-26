from __future__ import annotations

from typing import Optional, List, Annotated
from pydantic import BaseModel, EmailStr
from annotated_types import MinLen, MaxLen

from src.shemas.common import CompanyCommon
from src.shemas.position import PositionResponse
from src.shemas.task import TaskResponse


class UserBase(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False


class UserCreate(UserBase):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    password: str
    company_id: Optional[int] = None
    position_id: Optional[int] = None


class UserUpdate(UserBase):
    pass


class UserResponseRegister(UserBase):
    id: int
    # company: Optional['CompanyCommon'] = None
    # position: Optional['PositionResponse'] = None
    # authored_tasks: Optional[List['TaskResponse']] = []
    # responsible_tasks: Optional[List['TaskResponse']] = []

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
