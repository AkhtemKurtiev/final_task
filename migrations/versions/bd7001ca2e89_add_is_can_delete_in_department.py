"""add is_can_delete in department

Revision ID: bd7001ca2e89
Revises: 4105ad98ee68
Create Date: 2024-08-31 09:12:37.466284

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd7001ca2e89'
down_revision: Union[str, None] = '4105ad98ee68'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('departments', sa.Column('is_can_deleted', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('departments', 'is_can_deleted')
    # ### end Alembic commands ###
