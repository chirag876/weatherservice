from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import io
import logging
from app.database import get_db, create_tables
from app.services.weather_service import WeatherService
from app.services.export_service import ExportService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Weather Report Service",
    description="A service to fetch, store, and export weather data with charts",
    version="1.0.0"
)

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()
    logger.info("Database tables created successfully")

@app.get("/")
async def root():
    return {
        "message": "Weather Report Service API",
        "version": "1.0.0",
        "endpoints": [
            "/weather-report",
            "/export/excel", 
            "/export/pdf"
        ]
    }

@app.get("/weather-report")
async def get_weather_report(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    db: Session = Depends(get_db)
):
    # \"\"\"Fetch and store weather data for given coordinates\"\"\"
    try:
        result = await WeatherService.fetch_weather_data(lat, lon, db)
        return result
    except Exception as e:
        logger.error(f"Error in weather report endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/export/excel")
async def export_excel(
    lat: float = Query(None, description="Latitude (optional)"),
    lon: float = Query(None, description="Longitude (optional)"),
    db: Session = Depends(get_db)
):
    # Export weather data to Excel file
    try:
        excel_data = ExportService.generate_excel(db, lat, lon)
        
        # Create filename
        location_str = f"_lat_{lat}_lon_{lon}" if lat and lon else ""
        filename = f"weather_data{location_str}.xlsx"
        
        return StreamingResponse(
            io.BytesIO(excel_data),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        logger.error(f"Error in Excel export endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/export/pdf")
async def export_pdf(
    lat: float = Query(None, description="Latitude (optional)"),
    lon: float = Query(None, description="Longitude (optional)"),
    db: Session = Depends(get_db)
):
    # Export weather data as PDF report with chart
    try:
        pdf_data = ExportService.generate_pdf_report(db, lat, lon)
        
        # Create filename
        location_str = f"_lat_{lat}_lon_{lon}" if lat and lon else ""
        filename = f"weather_report{location_str}.pdf"
        
        return StreamingResponse(
            io.BytesIO(pdf_data),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        logger.error(f"Error in PDF export endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Weather Report Service is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)