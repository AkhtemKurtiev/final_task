from pydantic import BaseModel
from typing import List, Optional

from .department import DepartmentResponse
from .user import UserResponse


class CompanyBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    name: Optional[str] = None


class CompanyResponse(CompanyBase):
    id: int
    departments: Optional[List['DepartmentResponse']] = []
    employees: Optional[List['UserResponse']] = []
