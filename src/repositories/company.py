from src.models.company import Company
from src.utils.repository import SqlAlchemyRepository


class CompanyRepository(SqlAlchemyRepository):
    model = Company
