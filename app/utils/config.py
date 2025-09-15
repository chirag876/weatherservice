from datetime import datetime, timedelta


class Config:
    DATABASE_URL = "sqlite:///./weather_data.db"
    OPEN_METEO_BASE_URL = "https://api.open-meteo.com/v1/forecast"

    @staticmethod
    def get_past_2_days():
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=2)
        return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
