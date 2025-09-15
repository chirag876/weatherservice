from pydantic import BaseModel


class WeatherSchema(BaseModel):
    timestamp: str
    temperature: float
    humidity: float

    class Config:
        orm_mode = True
