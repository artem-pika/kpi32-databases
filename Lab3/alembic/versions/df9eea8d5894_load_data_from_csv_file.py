"""Load data from csv file

Revision ID: df9eea8d5894
Revises: 50c00d13e4a5
Create Date: 2025-04-04 09:03:23.793796

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pandas as pd


# revision identifiers, used by Alembic.
revision: str = 'df9eea8d5894'
down_revision: Union[str, None] = '50c00d13e4a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Fill the table with data."""
    data = pd.read_csv("./repository/GlobalWeatherRepository.csv")
    columns = ["country", "location_name", "last_updated", "sunrise", "wind_mph", "wind_kph", "wind_degree", "wind_direction"]
    data = data[columns]
    data.columns = ["country", "location_name", "date", "sunrise_time", "wind_mph", "wind_kph", "wind_degree", "wind_direction"]

    db_url = "postgresql+psycopg2://postgres:strong_password@localhost:5432/lab3"
    engine = sa.create_engine(db_url)
    data.to_sql("weather", engine, if_exists="append", index=False)

def downgrade() -> None:
    """Remove the data."""
    op.execute("TRUNCATE TABLE weather;")
