from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import func
from repository import orm

db_url = "postgresql+psycopg2://postgres:strong_password@localhost:5432/lab3"

def get_all_weather_info(country, date):
    country = country.lower().strip()
    date = date.strip()
    
    engine = create_engine(db_url)
    session = Session(engine)
    record = session.query(orm.Weather).join(orm.Wind).filter(
        func.lower(orm.Weather.country) == country, 
        func.date(orm.Weather.date) == date
    ).first()
    if record is None:
        result = None
    else:
        result = {
            "country": record.country,
            "location_name": record.location_name,
            "date": date,
            "wind_mph": float(record.wind.wind_mph),
            "wind_kph": float(record.wind.wind_kph),
            "wind_degree": record.wind.wind_degree,
            "wind_direction": record.wind.wind_direction,
            "go_outside": record.wind.go_outside,
        }
    session.close()

    return result