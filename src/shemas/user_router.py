from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class MessageResponse(BaseModel):
    message: str


class InviteResponse(BaseModel):
    message: str
    invite_token: str
