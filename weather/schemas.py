from typing import List

from ninja import Schema


class Coords(Schema):
    lat: float
    lon: float


class Weather(Schema):
    main: str
    description: str
    icon: str


class WeatherInfo(Schema):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: float
    humidity: float


class Location(Schema):
    country: str
    sunrise: int
    sunset: int


class CurrentWeather(Schema):
    coord: Coords
    weather: List[Weather]
    main: WeatherInfo
    sys: Location
    timezone: int
    name: str


class TimeWeather(Schema):
    main: WeatherInfo
    weather: List[Weather]


class Error(Schema):
    message: str
