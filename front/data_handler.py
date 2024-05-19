from typing import List
from urllib.parse import urljoin
from datetime import datetime, timedelta, timezone

import requests
from django.shortcuts import redirect

from front.errors import CityNotFound, EmptySearch, ForecastError
from front.models import CurrentWeather, SearchedCity, FavouriteLocation, TimeData
from weather import settings


def get_current_weather(query: str = settings.DEFAULT_CITY, units: str = "metric") -> CurrentWeather:
    try:
        result = requests.get(
            settings.CURRENT_WEATHER_API_URL,
            params={
                "q": query,
                "units": units,
                "appid": settings.WEATHER_API_KEY,
            },
        )

    except (requests.HTTPError, requests.ConnectionError) as e:
        print(e)
        raise ConnectionError()

    data = result.json()
    print(data)
    if data["cod"] != 200:
        raise CityNotFound()
    current_weather = CurrentWeather(**data)

    return current_weather


def check_weather_data(result) -> List[TimeData]:
    data = result.json()
    print(data)
    print(data["cod"])
    if data["cod"] != "200":
        raise ForecastError()

    time_data = [TimeData(**forecast) for forecast in data["list"]]
    print(data["cnt"])
    return time_data


def get_weather_forecast(lat: float, lon: float) -> List[TimeData]:
    try:
        result = requests.get(
            settings.FORECAST_API_URL,
            params={
                "lat": lat,
                "lon": lon,
                "appid": settings.WEATHER_API_KEY,
                "cnt": 8,
                "units": "metric"
            }
        )
    except (requests.HTTPError, requests.ConnectionError) as e:
        print(e)
        raise ConnectionError()

    forecasts = check_weather_data(result)
    return forecasts


def get_start_utc_time(hours_back: int) -> int:
    current_time_utc = datetime.now(timezone.utc)
    delta = timedelta(hours=hours_back)
    return int((current_time_utc - delta).timestamp())


def get_historical_data(lat: float, lon: float, units: str = "metric", cnt: int = 8, hours_back: int = 8) -> List[TimeData]:
    try:
        result = requests.get(
            settings.HISTORY_API_URL,
            params={
                "lat": lat,
                "lon": lon,
                "appid": settings.WEATHER_API_KEY,
                "units": units,
                "cnt": cnt,
                "type": "hour",
                "start": get_start_utc_time(hours_back),
            }
        )
    except (requests.HTTPError, requests.ConnectionError) as e:
        print(e)
        raise ConnectionError()

    historical = check_weather_data(result)
    return historical[::-1]


def is_users_favourite(current_weather: CurrentWeather, request) -> bool:
    favorite = False
    if current_weather and request.user.is_authenticated:
        favorite = FavouriteLocation.objects.filter(
            user=request.user, latitude=current_weather.coord.lat,
            longitude=current_weather.coord.lon
        ).exists()
    return favorite


def get_query_weather(request):
    error_message = None
    current_weather = None
    query = request.GET.get('query')
    if query:
        try:
            current_weather = get_current_weather(query)
        except CityNotFound:
            error_message = 'City not found'
    else:
        current_weather = get_current_weather()
    return current_weather, error_message


def get_user_favorites(user):
    favorites = FavouriteLocation.objects.filter(user=user)
    if not favorites:
        return None
    return favorites
