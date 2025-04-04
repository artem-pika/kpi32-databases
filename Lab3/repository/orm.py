from sqlalchemy import Column, Integer, String, DateTime, Time, Numeric
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Weather(Base):
    __tablename__ = "weather"
    
    id = Column(Integer, primary_key=True)
    country = Column(String(128))
    location_name = Column(String(128))
    date = Column(DateTime)
    sunrise_time = Column(Time)
    wind_mph = Column(Numeric(10, 2))
    wind_kph = Column(Numeric(10, 2))
    wind_degree = Column(Integer)
    wind_direction = Column(String(8))

