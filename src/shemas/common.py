from __future__ import annotations

from pydantic import BaseModel


class UserCommon(BaseModel):
    id: int
    email: str
    username: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


class CompanyCommon(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
