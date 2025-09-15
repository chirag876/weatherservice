import pandas as pd
from app.database import SessionLocal
from app.models import WeatherData


def generate_excel(file_path="weather_data.xlsx"):
    db = SessionLocal()
    records = db.query(WeatherData).all()
    db.close()

    if not records:
        return None

    data = [{"timestamp": r.timestamp, "temperature": r.temperature,
             "humidity": r.humidity} for r in records]

    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)
    return file_path
