from src.models.position import Position
from src.utils.repository import SqlAlchemyRepository


class PositionRepository(SqlAlchemyRepository):
    model = Position
