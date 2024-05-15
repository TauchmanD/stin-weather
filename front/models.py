from typing import List

from django.db import models
from pydantic import BaseModel
from django.contrib.auth.models import AbstractUser


# Create your models here.
class SearchedCity(BaseModel):
    name: str
    lat: float
    lon: float
    state: str


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


class Coords(BaseModel):
    lat: float
    lon: float


class CurrentWeather(BaseModel):
    coord: Coords
    weather: List[Weather]
    main: WeatherInfo
    sys: Location
    timezone: int
    name: str


class TimeData(BaseModel):
    main: WeatherInfo
    weather: List[Weather]


class WeatherUser(AbstractUser):
    # Add custom fields here
    favorite_locations = models.ManyToManyField('FavouriteLocation', blank=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    paying = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class FavouriteLocation(models.Model):
    user = models.ForeignKey(WeatherUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default="Old favourite")
    latitude = models.FloatField()
    longitude = models.FloatField()
