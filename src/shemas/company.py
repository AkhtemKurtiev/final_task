from __future__ import annotations

from pydantic import BaseModel
from typing import List, Optional

from src.shemas.common import UserCommon
from src.shemas.department import DepartmentResponse


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
