"""add Unique for Email - placeholder

Revision ID: 045f92239e9e
Revises: e064058f89cf
Create Date: 2026-04-21 22:52:06.943826

"""

from typing import Sequence, Union


revision: str = "045f92239e9e"
down_revision: Union[str, Sequence[str], None] = "3e378545ba79"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Placeholder - actual constraint already in 3e378545ba79
    pass


def downgrade() -> None:
    pass
