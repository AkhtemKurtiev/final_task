from sqlalchemy import (
    Column, Integer, String,
    Sequence, Index, func, select, update,
    ForeignKey
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

    company = relationship('Company', back_populates='departments')
    parent = relationship(
        'Department',
        primaryjoin=remote(path) == foreign(func.subpath(path, 0, -1)),
        backref='children',
        viewonly=True,
    )

    def __init__(self, name, parent=None, company_id=None):
        self.name = name
        self.company_id = company_id
        self.parent = parent
        self.path = None

    async def initialize(self, session: AsyncSession):
        result = await session.execute(id_seq)
        self.id = result.scalar()

        lthree_id = Ltree(str(self.id))
        if self.parent is None:
            self.path = lthree_id
        else:
            self.path = self.parent.path + '.' + str(self.id)

    __table_args__ = (
        Index('ix_departments_path', path, postgresql_using='gist'),
    )

    async def delete(self, session: AsyncSession):
        parent_stmt = select(Department).filter(
                func.subpath(self.path, 0, -1) == Department.path
            )
        result = await session.execute(parent_stmt)
        parent_node = result.scalars().first()

        if parent_node:
            for child in self.children:
                new_path = parent_node.path + '.' + str(child.id)
                update_stmt = update(Department).where(
                    Department.id == child.id
                ).values(path=new_path)
                await session.execute(update_stmt)

        await session.delete(self)
        await session.commit()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Department({self.name})'
