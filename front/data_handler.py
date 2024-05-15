from typing import List
from urllib.parse import urljoin

import requests
from django.shortcuts import redirect

from front.errors import CityNotFound, EmptySearch
from front.models import CurrentWeather, SearchedCity, FavouriteLocation
from weather import settings


def get_current_weather(query: str = settings.DEFAULT_CITY) -> CurrentWeather:
    try:
        result = requests.get(
            settings.CURRENT_WEATHER_API_URL,
            params={
                "q": query,
                "units": "metric",
                "appid": settings.WEATHER_API_KEY,
            },
        )

    except (requests.HTTPError, requests.ConnectionError) as e:
        print(e)
        raise ValueError()

    data = result.json()
    if data["cod"] != 200:
        raise CityNotFound()
    current_weather = CurrentWeather(**data)

    return current_weather


def get_users_favorites(user) -> List[FavouriteLocation]:
    favorite_locations = FavouriteLocation.objects.filter(user=user)
    return favorite_locations

