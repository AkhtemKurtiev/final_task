"""fix position model depatment_id SET_NULL

Revision ID: f034fc59287b
Revises: bd7001ca2e89
Create Date: 2024-09-01 11:57:47.118861

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f034fc59287b'
down_revision: Union[str, None] = 'bd7001ca2e89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('positions_department_id_fkey', 'positions', type_='foreignkey')
    op.create_foreign_key(None, 'positions', 'departments', ['department_id'], ['id'], ondelete='SET NULL')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'positions', type_='foreignkey')
    op.create_foreign_key('positions_department_id_fkey', 'positions', 'departments', ['department_id'], ['id'])
    # ### end Alembic commands ###
