from src.models.position import Position
from src.utils.repository import SqlAlchemyRepository


class PositionRepository(SqlAlchemyRepository):
    model = Position

    async def add_position(self, name, department):
        new_position = self.model(name=name, department=department)
        self.session.add(new_position)
        return new_position

    async def get_position(self, position_id):
        return await self.session.get(self.model, position_id)
