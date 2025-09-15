# Weather Report Service

A FastAPI-based service that fetches time-series weather data from the Open-Meteo API and generates Excel files and PDF reports with charts.

## Features

- ✅ Fetch weather data from Open-Meteo MeteoSwiss API
- ✅ Store data in SQLite database
- ✅ REST API endpoints for data fetching and export
- ✅ Excel export with weather data
- ✅ PDF report generation with temperature and humidity charts
- ✅ Proper error handling and logging
- ✅ Clean project structure

## Project Structure

```
weather-report-service/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application and routes
│   ├── models.py            # SQLAlchemy models
│   ├── database.py          # Database configuration
│   ├── services/
│   │   ├── __init__.py
│   │   ├── weather_service.py    # Weather API integration
│   │   └── export_service.py     # Excel and PDF export logic
│   └── utils/
│       ├── __init__.py
│       └── config.py        # Configuration settings
├── requirements.txt         # Python dependencies
├── README.md
└── run.py                  # Application runner
```

## Installation & Setup

1. **Clone/Create the project directory:**
   ```bash
   mkdir weather-report-service
   cd weather-report-service
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python run.py
   ```

   Or alternatively:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## API Endpoints

### 1. Fetch Weather Data
```http
GET /weather-report?lat={latitude}&lon={longitude}
```

**Example:**
```bash
curl "http://localhost:8000/weather-report?lat=47.37&lon=8.55"
```

**Response:**
```json
{
  "message": "Successfully fetched and stored 48 weather records"
}
```

### 2. Export to Excel
```http
GET /export/excel?lat={latitude}&lon={longitude}
```

**Example:**
```bash
curl -o weather_data.xlsx "http://localhost:8000/export/excel?lat=47.37&lon=8.55"
```

Returns an Excel file with columns: `timestamp`, `temperature_2m`, `relative_humidity_2m`, `latitude`, `longitude`

### 3. Export PDF Report
```http
GET /export/pdf?lat={latitude}&lon={longitude}
```

**Example:**
```bash
curl -o weather_report.pdf "http://localhost:8000/export/pdf?lat=47.37&lon=8.55"
```

Returns a PDF report with:
- Title and metadata (location, date range)
- Line charts showing temperature and humidity over time

### 4. Health Check
```http
GET /health
```

### 5. API Documentation
- Interactive docs: http://localhost:8000/docs
- OpenAPI schema: http://localhost:8000/openapi.json

## Usage Example

1. **Start the server:**
   ```bash
   python run.py
   ```

2. **Fetch weather data for Zurich:**
   ```bash
   curl "http://localhost:8000/weather-report?lat=47.37&lon=8.55"
   ```

3. **Download Excel report:**
   ```bash
   curl -o zurich_weather.xlsx "http://localhost:8000/export/excel?lat=47.37&lon=8.55"
   ```

4. **Download PDF report:**
   ```bash
   curl -o zurich_weather.pdf "http://localhost:8000/export/pdf?lat=47.37&lon=8.55"
   ```

## Dependencies

- **FastAPI**: Web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **pandas**: Data manipulation and analysis
- **openpyxl**: Excel file generation
- **matplotlib**: Chart generation
- **weasyprint**: PDF generation
- **httpx**: HTTP client for API calls

## Features Implemented

✅ **API Integration**: Fetches data from Open-Meteo MeteoSwiss API for past 2 days  
✅ **Database Storage**: SQLite database with proper schema  
✅ **REST API**: Clean FastAPI endpoints with proper error handling  
✅ **Excel Export**: Generates .xlsx files with time-series data  
✅ **PDF Reports**: Creates PDF with charts using matplotlib and weasyprint  
✅ **Error Handling**: Comprehensive error handling and logging  
✅ **Documentation**: Auto-generated API docs with FastAPI  

## Notes

- The service automatically fetches the last 2 days of weather data
- Data is stored in SQLite database (`weather_data.db`)
- Charts show temperature and humidity trends over time
- Export endpoints support optional lat/lon filtering
- All endpoints include proper error handling and logging

## Testing the Service

Visit http://localhost:8000/docs for interactive API documentation where you can test all endpoints directly from your browser.