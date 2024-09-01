from sqlalchemy.future import select

from src.models.department import Department
from src.utils.repository import SqlAlchemyRepository


class DepartmentRepository(SqlAlchemyRepository):
    model = Department

    async def get_department(self, id):
        return await self.session.get(self.model, id)

    async def get_department_filter(self, company_id, is_can_deleted):
        result = await self.session.execute(
                    select(self.model).filter(
                        self.model.company_id == company_id,
                        self.model.is_can_deleted == is_can_deleted,
                    )
                )
        return result.scalars().first()

    async def add_department(
            self,
            department_name,
            company_id,
            parent=None,
            is_can_deleted=True
    ):

        new = self.model(
                name=department_name,
                company_id=company_id,
                parent=parent,
                is_can_deleted=is_can_deleted
            )
        await new.initialize(self.session)
        self.session.add(new)
        await self.session.commit()
        await self.session.refresh(new)
        return new

    async def update_department(self, department):
        self.session.add(department)
        await self.session.commit()
        await self.session.refresh(department)

    async def delete_department(self, department):
        await department.delete_department(self.session)
