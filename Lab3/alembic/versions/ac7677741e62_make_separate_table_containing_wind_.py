"""Make separate table containing wind measurements

Revision ID: ac7677741e62
Revises: df9eea8d5894
Create Date: 2025-04-04 09:54:15.537625

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac7677741e62'
down_revision: Union[str, None] = 'df9eea8d5894'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'wind',
        sa.Column('weather_id', sa.Integer(), nullable=False),
        sa.Column('wind_mph', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('wind_kph', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('wind_degree', sa.Integer(), nullable=True),
        sa.Column('wind_direction', sa.String(length=8), nullable=True),
        sa.ForeignKeyConstraint(['weather_id'], ['weather.id'], ),
        sa.PrimaryKeyConstraint('weather_id')
    )

    # Move wind data from 'weather' to 'wind' table
    op.execute("""INSERT INTO wind (weather_id, wind_mph, wind_kph, wind_degree, wind_direction)
SELECT id, wind_mph, wind_kph, wind_degree, wind_direction
FROM weather;""")

    op.drop_column('weather', 'wind_kph')
    op.drop_column('weather', 'wind_mph')
    op.drop_column('weather', 'wind_degree')
    op.drop_column('weather', 'wind_direction')


def downgrade() -> None:
    """Downgrade schema."""
    pass