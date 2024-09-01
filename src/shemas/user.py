from __future__ import annotations

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, EmailStr
from typing import Annotated, Optional


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

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResgister(BaseModel):
    email: EmailStr
    username: Annotated[str, MinLen(3), MaxLen(20)]
    password: str
    username: str
    first_name: str
    last_name: str
    is_admin: Optional[bool] = True
    company_name: str


class UserAdminCreateEmployee(BaseModel):
    email: EmailStr
    username: Annotated[str, MinLen(3), MaxLen(20)]
    username: str
    first_name: str
    last_name: str
    is_admin: Optional[bool] = False


class UserName(BaseModel):
    first_name: str
    last_name: str
