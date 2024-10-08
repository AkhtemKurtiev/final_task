"""add user password nullable

Revision ID: 8fbb39948754
Revises: a2cf07ea9dee
Create Date: 2024-08-27 11:45:18.075834

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8fbb39948754'
down_revision: Union[str, None] = 'a2cf07ea9dee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'hashed_password',
               existing_type=postgresql.BYTEA(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'hashed_password',
               existing_type=postgresql.BYTEA(),
               nullable=False)
    # ### end Alembic commands ###
