from typing import Optional, List, Annotated

from pydantic import BaseModel, EmailStr
from annotated_types import MinLen, MaxLen

from .company import CompanyResponse
from .position import PositionResponse
from .task import TaskResponse


class UserBase(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False


class UserCreate(UserBase):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    password: bytes
    company_id: int
    position_id: int


class UserUpdate(UserBase):
    pass


class UserResponse():
    id: int
    company: Optional['CompanyResponse']
    position: Optional['PositionResponse']
    authored_tasks: Optional[List['TaskResponse']] = []
    responsible_tasks: Optional[List['TaskResponse']] = []

    class Config:
        orm_mode = True
