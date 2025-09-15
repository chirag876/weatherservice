import matplotlib.pyplot as plt
import pandas as pd
from app.database import SessionLocal
from app.models import WeatherData
from weasyprint import HTML
from datetime import datetime


def generate_pdf(file_path="weather_report.pdf", lat=None, lon=None):
    db = SessionLocal()
    records = db.query(WeatherData).all()
    db.close()

    if not records:
        raise ValueError(
            "No weather data available. Please call /weather-report first.")

    df = pd.DataFrame([{"timestamp": r.timestamp, "temperature": r.temperature,
                        "humidity": r.humidity} for r in records])

    # Ensure timestamp is sorted
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    # Chart
    plt.figure(figsize=(10, 5))
    plt.plot(df["timestamp"], df["temperature"],
             label="Temperature (°C)", color="red")
    plt.plot(df["timestamp"], df["humidity"],
             label="Humidity (%)", color="blue")
    plt.xticks(rotation=45)
    plt.xlabel("Time")
    plt.ylabel("Values")
    plt.legend()
    plt.tight_layout()
    plt.savefig("chart.png")
    plt.close()

    # Date range
    start = df["timestamp"].min().strftime("%Y-%m-%d %H:%M")
    end = df["timestamp"].max().strftime("%Y-%m-%d %H:%M")
    generated_on = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    html_content = f"""
    <html>
    <head><title>Weather Report</title></head>
    <body>
        <h1>Weather Report</h1>
        <p><b>Location:</b> Lat {lat}, Lon {lon}</p>
        <p><b>Date Range:</b> {start} → {end}</p>
        <p><b>Generated On:</b> {generated_on}</p>
        <img src="chart.png" width="600">
    </body>
    </html>
    """
    HTML(string=html_content).write_pdf(file_path)
    return file_path
