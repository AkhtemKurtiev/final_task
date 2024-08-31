from src.models.user import User
from src.utils.repository import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):
    model = User
