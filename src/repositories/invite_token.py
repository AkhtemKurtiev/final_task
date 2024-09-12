from sqlalchemy.future import select

from src.models.invite_token import InviteToken
from src.utils.repository import SqlAlchemyRepository


class InviteTokenRepository(SqlAlchemyRepository):
    model = InviteToken

    async def add_invite_token(self, invite_token, user_id):

        new = self.model(
                token=invite_token,
                user_id=user_id
            )

        self.session.add(new)
        return new

    async def get_invite_token_filter(self, token):
        result = await self.session.execute(
                select(self.model).filter(self.model.token == token)
            )
        return result.scalars().first()

    async def delete_invite_token(self, invite_token):
        await self.session.delete(invite_token)
