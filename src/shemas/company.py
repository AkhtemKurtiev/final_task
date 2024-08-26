from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING
from pydantic import BaseModel

from src.shemas.department import DepartmentResponse
from src.shemas.common import UserCommon


class CompanyBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    name: Optional[str] = None


class CompanyResponse(CompanyBase):
    id: int
    departments: Optional[List['DepartmentResponse']] = []
    employees: Optional[List['UserCommon']] = []
