from src.shemas.company import CompanyBase
from src.shemas.user import UserBase


class CompanyCommon(CompanyBase):
    pass


class UserCommon(UserBase):
    id: int

    class Config:
        from_attributes = True
