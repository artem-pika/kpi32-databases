"""Fill 'go_outside' column

Revision ID: 93ee99bd0b66
Revises: 79f4f8ec6949
Create Date: 2025-04-04 12:40:30.845263

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlalchemy.orm import Session
from repository import orm
from domain.weather import Wind

# revision identifiers, used by Alembic.
revision: str = '93ee99bd0b66'
down_revision: Union[str, None] = '79f4f8ec6949'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Fill 'go_outside' column with values."""
    
    db_url = "postgresql+psycopg2://postgres:strong_password@localhost:5432/lab3"
    engine = sa.create_engine(db_url)
    session = Session(engine)
    all_records = session.query(orm.Wind).all()
    for record in all_records:
        wind = Wind(
            kph=record.wind_kph, 
            mph=record.wind_mph, 
            degree=record.wind_degree, 
            direction=record.wind_direction
        )
        record.go_outside = wind.go_outside()
    session.commit()
    session.close()


def downgrade() -> None:
    """Downgrade schema."""
    pass
