from fastapi import HTTPException
from sqlalchemy import (
    Column, Integer, String,
    Sequence, Index, func, select, update,
    ForeignKey, text, delete, cast, Boolean
)
from sqlalchemy.orm import relationship, remote, foreign
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_utils import LtreeType, Ltree

from src.database.db import BaseModel

id_seq = Sequence('departments_id_seq')


class Department(BaseModel):
    __tablename__ = 'departments'

    id = Column(Integer, id_seq, primary_key=True)
    name = Column(String, nullable=False)
    path: LtreeType = Column(LtreeType, nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'))
    is_can_deleted = Column(Boolean, default=True)

    manager_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    manager = relationship('User', backref='managed_departments')

    company = relationship('Company', back_populates='departments')
    positions = relationship('Position', back_populates='department')

    parent = relationship(
        'Department',
        primaryjoin=remote(path) == foreign(func.subpath(path, 0, -1)),
        backref='children',
        viewonly=True,
    )

    def __init__(
            self, name, parent=None, company_id=None, is_can_deleted=True
    ):
        self.name = name
        self.company_id = company_id
        self.parent = parent
        self.is_can_deleted = is_can_deleted
        self.path = None

    async def initialize(self, session: AsyncSession):
        self.id = await session.scalar(id_seq)

        if self.parent and self.parent.path:
            self.path = Ltree(f"{self.parent.path}.{self.id}")
        elif self.parent is None:
            self.path = Ltree(str(self.id))
        else:
            raise ValueError("Invalid parent path")

    __table_args__ = (
        Index('ix_departments_path', path, postgresql_using='gist'),
    )

    # SQL запросы не безопасны. Придумайте ORM реализацию перед использованием!
    async def delete_department(self, session: AsyncSession):

        if not self.is_can_deleted:
            raise HTTPException(
                status_code=400,
                detail="This department can't be deleted."
            )

        parent_path_str = str(self.path)

        await session.execute(
            text(
                """
                UPDATE departments
                SET path = text2ltree(
                    concat(
                        ltree2text(subpath(:parent_path, 0, -1)),
                        '.',
                        ltree2text(subpath(departments.path, nlevel(:parent_path)))
                    )
                )
                WHERE departments.path <@ :parent_path
                AND departments.path != :parent_path
                """
            ),
            {'parent_path': parent_path_str}
        )

        await session.execute(
            delete(self.__class__).where(self.__class__.id == self.id)
        )

        await session.commit()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Department({self.name})'
