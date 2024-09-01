from pydantic import BaseModel
from typing import List, Optional


class DepartmentBase(BaseModel):
    name: str
    path: str
    company_id: int


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(DepartmentBase):
    pass


class DepartmentResponse(DepartmentBase):
    id: int
    children: Optional[List['DepartmentResponse']] = []

    class Config:
        orm_mode = True
