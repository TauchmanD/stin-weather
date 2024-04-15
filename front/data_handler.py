from urllib.parse import urljoin

import requests

from front.models import CurrentWeather
from weather import settings


def get_current_weather(lat: float, lon: float) -> CurrentWeather:
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
