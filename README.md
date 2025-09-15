# Weather Service

This project is a weather service application built with Python and FastAPI. It fetches weather data from the Open-Meteo API, stores it in a SQLite database, and provides endpoints to export the data as Excel or PDF reports.

## Project Structure

```
weather-service/
├── README.md
├── requirements.txt
├── weather_data.xlsx
├── weather.db
└── app/
    ├── __init__.py
    ├── config.py
    ├── database.py
    ├── main.py
    ├── models.py
    ├── schemas.py
    ├── services/
    │   ├── export_service.py
    │   └── weather_service.py
    └── utils/
        ├── chart_generator.py
        ├── excel_generator.py
        └── pdf_generator.py
```

## Features

- Fetches weather data (temperature and humidity) for a given latitude and longitude from Open-Meteo.
- Stores weather data in a local SQLite database.
- Exports weather data as Excel or PDF reports.
- Generates charts for visual representation in reports.

## Installation

1. Clone the repository and navigate to the project directory.
2. Install the required dependencies:

    ```
    pip install -r requirements.txt
    ```

## Usage

1. Start the FastAPI server:

    ```
    uvicorn app.main:app --reload
    ```

2. Available endpoints:
    - `GET /weather-report?lat={latitude}&lon={longitude}`  
      Fetch and store weather data for the specified location.
    - `GET /export/excel`  
      Download the weather data as an Excel file.
    - `GET /export/pdf`  
      Download the weather report as a PDF file.

## Configuration

- API and database settings are in [`app/config.py`](app/config.py).

## License

This project is licensed under the MIT License.
