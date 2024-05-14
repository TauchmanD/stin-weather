from urllib.parse import urljoin

import requests

from front.errors import CityNotFound, EmptySearch
from front.models import CurrentWeather, SearchedCity
from weather import settings


def get_lat_long_from_search(search_string: str = "Liberec") -> SearchedCity:
    if search_string is None:
        raise EmptySearch
    try:
        result = requests.get(
            settings.GEOCODING_API_URL,
            params={
                "q": search_string,
                "limit": 1,
                "appid": settings.WEATHER_API_KEY
            }
        )

    except (requests.HTTPError, requests.ConnectionError) as e:
        print(e)
        raise ValueError()

    locations = [SearchedCity(**location) for location in result.json()]
    print(locations)
    if len(locations) == 0:
        raise CityNotFound

    print(locations)

    return locations[0]


def get_current_weather(lat: float = 50.77, lon: float = 15.05) -> CurrentWeather:
    try:
        result = requests.get(
            settings.CURRENT_WEATHER_API_URL,
            params={
                "lat": lat,
                "lon": lon,
                "units": "metric",
                "appid": settings.WEATHER_API_KEY,
            },
        )

    except (requests.HTTPError, requests.ConnectionError) as e:
        print(e)
        raise ValueError()

    current_weather = CurrentWeather(**result.json())

    return current_weather
