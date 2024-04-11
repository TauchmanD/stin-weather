from typing import List

from django.db import models
from pydantic import BaseModel

# Create your models here.


class Weather(BaseModel):
    main: str
    description: str
    icon: str


class WeatherInfo(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: float
    humidity: float


class Location(BaseModel):
    country: str
    sunrise: int
    sunset: int


class CurrentWeather(BaseModel):
    weather: List[Weather]
    main: WeatherInfo
    sys: Location
    timezone: int
    name: str
