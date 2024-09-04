from typing import Optional

from pydantic import BaseModel


class DepartmentPathResponse(BaseModel):
    path: str


class DepartmentResponse(BaseModel):
    id: int
    name: str
    company_id: Optional[int]
    is_can_deleted: bool
    manager_id: Optional[int]
    path: DepartmentPathResponse


class PositionResponse(BaseModel):
    id: int
    name: str
    department_id: int

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    message: str


class AssignManagerResponse(BaseModel):
    message: str
    department: str
    manager: str
