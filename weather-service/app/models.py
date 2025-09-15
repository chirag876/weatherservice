from sqlalchemy import Column, Integer, Float, String
from app.database import Base


class WeatherData(Base):
    __tablename__ = "weather_data"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
