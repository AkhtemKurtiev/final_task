"""fix user password in bytes

Revision ID: c7b7791fda29
Revises: 3b8ce6a8e7c9
Create Date: 2024-08-26 11:28:30.595345

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7b7791fda29'
down_revision: Union[str, None] = '3b8ce6a8e7c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Explicitly convert the column using 'USING'
    op.execute("""
        ALTER TABLE "user" 
        ALTER COLUMN hashed_password 
        TYPE BYTEA 
        USING hashed_password::bytea
    """)


def downgrade():
    # Reverse the process to String
    op.execute("""
        ALTER TABLE "user" 
        ALTER COLUMN hashed_password 
        TYPE VARCHAR 
        USING hashed_password::VARCHAR
    """)
