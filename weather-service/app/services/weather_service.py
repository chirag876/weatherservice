import requests
from datetime import datetime, timedelta
from app.models import WeatherData
from app.database import SessionLocal
from app.config import OPEN_METEO_URL


def fetch_and_store_weather(lat: float, lon: float):
    db = SessionLocal()
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=2)

    url = (f"{OPEN_METEO_URL}?latitude={lat}&longitude={lon}"
           f"&start_date={start_date}&end_date={end_date}"
           f"&hourly=temperature_2m,relative_humidity_2m")

    response = requests.get(url)
    data = response.json()

    hourly = data.get("hourly", {})
    timestamps = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    hums = hourly.get("relative_humidity_2m", [])

    inserted = 0
    for ts, t, h in zip(timestamps, temps, hums):
        if ts and t is not None and h is not None:
            # check if already exists
            exists = db.query(WeatherData).filter(
                WeatherData.timestamp == ts).first()
            if not exists:
                entry = WeatherData(timestamp=ts, temperature=t, humidity=h)
                db.add(entry)
                inserted += 1

    db.commit()
    db.close()
    return {"message": f"{inserted} weather records stored successfully"}
