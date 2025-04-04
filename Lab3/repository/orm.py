from sqlalchemy import Column, Integer, String, DateTime, Time, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Weather(Base):
    __tablename__ = "weather"
    
    id = Column(Integer, primary_key=True)
    country = Column(String(128))
    location_name = Column(String(128))
    date = Column(DateTime)
    sunrise_time = Column(Time)
    wind = relationship("Wind", back_populates="weather", uselist=False)

class Wind(Base):
    __tablename__ = "wind"

    weather_id = Column(Integer, ForeignKey("weather.id"), primary_key=True)
    wind_mph = Column(Numeric(10, 2))
    wind_kph = Column(Numeric(10, 2))
    wind_degree = Column(Integer)
    wind_direction = Column(String(8))
    go_outside = Column(Boolean)
    weather = relationship("Weather", back_populates="wind")