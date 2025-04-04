"""Add 'go_outside' boolean column

Revision ID: 79f4f8ec6949
Revises: ac7677741e62
Create Date: 2025-04-04 12:36:17.378002

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79f4f8ec6949'
down_revision: Union[str, None] = 'ac7677741e62'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('wind', sa.Column('go_outside', sa.Boolean(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('wind', 'go_outside')
