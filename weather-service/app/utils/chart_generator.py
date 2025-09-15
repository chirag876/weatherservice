import matplotlib.pyplot as plt
from app.database import SessionLocal
from app.models import WeatherData


def generate_chart(image_path="chart.png"):
    session = SessionLocal()
    records = session.query(WeatherData).order_by(
        WeatherData.timestamp).limit(48).all()
    session.close()

    timestamps = [r.timestamp for r in records]
    temps = [r.temperature for r in records]
    hums = [r.humidity for r in records]

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, temps, label="Temperature (°C)", color="red")
    plt.plot(timestamps, hums, label="Humidity (%)", color="blue")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(image_path)
    plt.close()
    return image_path
