from fastapi import FastAPI
from app.database import Base, engine
from app.services.weather_service import fetch_and_store_weather
from app.services.export_service import export_excel, export_pdf

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/weather-report")
def weather_report(lat: float, lon: float):
    return fetch_and_store_weather(lat, lon)


@app.get("/export/excel")
def export_excel_report():
    return export_excel()


@app.get("/export/pdf")
def export_pdf_report():
    return export_pdf()
