from sqlalchemy import create_engine
from repository.orm import Base
import pandas as pd

postgre_engine = create_engine("postgresql+psycopg2://postgres:strong_password@localhost:5432/lab3")
mysql_engine = create_engine("mysql+mysqlconnector://root:strong_password@localhost/lab3")

# Create tables in mysql database
Base.metadata.create_all(mysql_engine)

# Migrate 'weather' table
data = pd.read_sql_table("weather", postgre_engine)
data.to_sql("weather", mysql_engine, if_exists="append", index=False)

# Migrate 'wind' table
data = pd.read_sql_table("wind", postgre_engine)
data.to_sql("wind", mysql_engine, if_exists="append", index=False)