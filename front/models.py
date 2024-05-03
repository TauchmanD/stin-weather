from typing import List

from django.db import models
from pydantic import BaseModel
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

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


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)  # This hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class WeatherUser(AbstractBaseUser):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class FavouriteLocation(models.Model):
    user = models.ForeignKey(WeatherUser, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
