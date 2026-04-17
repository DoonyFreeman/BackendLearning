"""initial migration

Revision ID: 704574d025af
Revises: 
Create Date: 2026-04-17 12:01:43.832165

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



revision: str = '704574d025af'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:


    op.create_table('hotels',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('location', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )



def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table('hotels')

