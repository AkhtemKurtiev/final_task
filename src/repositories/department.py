from src.models.department import Department
from src.utils.repository import SqlAlchemyRepository


class DepartmentRepository(SqlAlchemyRepository):
    model = Department
