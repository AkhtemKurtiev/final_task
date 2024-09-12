from sqlalchemy.future import select

from src.models.user import User
from src.utils.repository import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):
    model = User

    async def get_user_by_filter_email(self, email):
        result = await self.session.execute(
            select(self.model).filter(self.model.email == email)
        )
        return result.scalars().first()

    async def get_user_by_filter_id(self, user_id):
        result = await self.session.execute(
            select(self.model).filter(self.model.id == user_id)
        )
        return result.scalars().first()

    async def add_user(self, new_user, hashed_password, company_id):
        new = self.model(
                email=new_user.email,
                first_name=new_user.first_name,
                last_name=new_user.last_name,
                username=new_user.username,
                hashed_password=hashed_password,
                company_id=company_id,
                is_admin=True
            )

        self.session.add(new)
        return new

    async def add_user_first_step(self, new_user, company_id):
        new = self.model(
                email=new_user.email,
                first_name=new_user.first_name,
                last_name=new_user.last_name,
                username=new_user.username,
                company_id=company_id,
                is_admin=False,
                is_active=False
            )

        self.session.add(new)
        return new

    async def update_user(self, user):
        self.session.add(user)
        return user
