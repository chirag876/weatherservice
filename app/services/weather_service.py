import httpx
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import WeatherData
from app.utils.config import Config
import logging

logger = logging.getLogger(__name__)

class WeatherService:
    
    @staticmethod
    async def fetch_weather_data(latitude: float, longitude: float, db: Session):
        # Fetch weather data from Open-Meteo API and store in database
        
        start_date, end_date = Config.get_past_2_days()
        
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "temperature_2m,relative_humidity_2m",
            "start_date": start_date,
            "end_date": end_date,
            "timezone": "auto"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(Config.OPEN_METEO_BASE_URL, params=params)
                response.raise_for_status()
                data = response.json()
                
                # Clear existing data for this location
                db.query(WeatherData).filter(
                    WeatherData.latitude == latitude,
                    WeatherData.longitude == longitude
                ).delete()
                
                # Process and store the data
                hourly_data = data.get("hourly", {})
                timestamps = hourly_data.get("time", [])
                temperatures = hourly_data.get("temperature_2m", [])
                humidity = hourly_data.get("relative_humidity_2m", [])
                
                weather_records = []
                for i in range(len(timestamps)):
                    if temperatures[i] is not None and humidity[i] is not None:
                        weather_record = WeatherData(
                            timestamp=datetime.fromisoformat(timestamps[i].replace('Z', '+00:00')),
                            latitude=latitude,
                            longitude=longitude,
                            temperature_2m=temperatures[i],
                            relative_humidity_2m=humidity[i]
                        )
                        weather_records.append(weather_record)
                
                db.add_all(weather_records)
                db.commit()
                
                logger.info(f"Stored {len(weather_records)} weather records for lat:{latitude}, lon:{longitude}")
                return {"message": f"Successfully fetched and stored {len(weather_records)} weather records"}
                
            except httpx.HTTPError as e:
                logger.error(f"HTTP error occurred: {e}")
                raise Exception(f"Failed to fetch weather data: {e}")
            except Exception as e:
                logger.error(f"Error processing weather data: {e}")
                raise Exception(f"Error processing weather data: {e}")
    
    @staticmethod
    def get_last_48_hours_data(db: Session, latitude: float = None, longitude: float = None):
        # Get the last 48 hours of weather data
        query = db.query(WeatherData)
        
        if latitude is not None and longitude is not None:
            query = query.filter(
                WeatherData.latitude == latitude,
                WeatherData.longitude == longitude
            )
        
        # Get data from last 48 hours
        cutoff_time = datetime.now() - timedelta(hours=48)
        query = query.filter(WeatherData.timestamp >= cutoff_time)
        query = query.order_by(WeatherData.timestamp.asc())
        
        return query.all()