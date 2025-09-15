from sqlalchemy import Column, Integer, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    temperature_2m = Column(Float, nullable=False)
    relative_humidity_2m = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<WeatherData(timestamp={self.timestamp}, temp={self.temperature_2m}, humidity={self.relative_humidity_2m})>"
