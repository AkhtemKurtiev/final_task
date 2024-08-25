from pydantic import BaseModel


class PositionBase(BaseModel):
    name: str


class PositionCreate(PositionBase):
    pass


class PositionUpdate(PositionBase):
    pass


class PositionResponse(PositionBase):
    id: int

    class Config:
        orm_mode = True
