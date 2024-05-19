from typing import List, Optional, Any

from django.http import HttpRequest
from ninja import NinjaAPI
from ninja.security import APIKeyHeader

from front.errors import CityNotFound
from . import settings
from .schemas import CurrentWeather, Error, TimeWeather
from front.data_handler import get_current_weather, get_historical_data

api = NinjaAPI()


class ApiKey(APIKeyHeader):
    param_name = "user-api-key"

    def authenticate(self, request: HttpRequest, key: Optional[str]) -> Optional[Any]:
        if key == settings.USER_API_KEY:
            return key


api_key = ApiKey()


@api.get("/health")
def health(request):
    return {"status": "ok"}


@api.get("/current-weather", response={200: CurrentWeather, 404: Error, 400: Error}, auth=api_key)
def current_weather(request, city_name: str, units: str = "metric"):
    try:
        weather = get_current_weather(city_name, units)
    except CityNotFound:
        return 404, {"message": "City not found"}
    except ConnectionError:
        return 400, {"message": "Connection error"}
    return weather


@api.get("/historical-weather", response={200: List[TimeWeather], 404: Error, 400: Error}, auth=api_key)
def historical_weather(request, latitude: float, longitude: float, units: str = "metric", limit: int = 8, hours_back: int = 8):
    try:
        weather = get_historical_data(latitude, longitude, units, limit, hours_back)
    except ConnectionError:
        return 400, {"message": "Connection error"}
    return weather
