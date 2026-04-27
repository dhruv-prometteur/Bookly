"""merge heads

Revision ID: 86f414f06157
Revises: 728706004aca, c0f2eb412bc0
Create Date: 2026-04-21 17:03:11.893678

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '86f414f06157'
down_revision: Union[str, Sequence[str], None] = ('728706004aca', 'c0f2eb412bc0')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
