"""Initialize table schema

Revision ID: 50c00d13e4a5
Revises: 
Create Date: 2025-04-03 20:00:37.811385

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50c00d13e4a5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'weather',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('country', sa.String(length=128), nullable=True),
        sa.Column('location_name', sa.String(length=128), nullable=True),
        sa.Column('date', sa.DateTime(), nullable=True),
        sa.Column('sunrise_time', sa.Time(), nullable=True),
        sa.Column('wind_mph', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('wind_kph', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('wind_degree', sa.Integer(), nullable=True),
        sa.Column('wind_direction', sa.String(length=8), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('weather')
