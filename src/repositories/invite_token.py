from src.models.invite_token import InviteToken
from src.utils.repository import SqlAlchemyRepository


class InviteTokenRepository(SqlAlchemyRepository):
    model = InviteToken
