from src.models.company import Company
from src.utils.repository import SqlAlchemyRepository


class CompanyRepository(SqlAlchemyRepository):
    model = Company

    async def add_company(self, name):
        new = self.model(name=name)
        self.session.add(new)
        await self.session.commit()
        await self.session.refresh(new)
        return new
