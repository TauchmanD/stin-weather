import pytest
import requests
from unittest.mock import patch, Mock, MagicMock
from datetime import datetime, timezone, timedelta

from front.errors import CityNotFound, EmptySearch, ForecastError
from front.models import CurrentWeather, SearchedCity, FavouriteLocation, TimeData
from front.user_handling import register_user
from weather import settings
from front.data_handler import (
    get_current_weather,
    check_weather_data,
    get_weather_forecast,
    get_start_utc_time,
    get_historical_data,
    is_users_favourite,
    get_query_weather,
    get_user_favorites
)


@pytest.fixture
def mock_requests_get():
    with patch('front.data_handler.requests.get') as mock_get:
        yield mock_get


def test_get_current_weather_success(mock_requests_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "cod": 200,
        "coord": {"lat": 51.5074, "lon": -0.1278},
        "weather": [{"main": "Clear", "description": "clear sky", "icon": "01d"}],
        "main": {"temp": 15.0, "feels_like": 14.0, "temp_min": 10.0, "temp_max": 20.0, "pressure": 1012, "humidity": 50},
        "sys": {"country": "GB", "sunrise": 1623223620, "sunset": 1623277260},
        "timezone": 3600,
        "name": "London"
    }
    mock_requests_get.return_value = mock_response

    weather = get_current_weather("London")
    assert isinstance(weather, CurrentWeather)
    assert weather.coord.lat == 51.5074
    assert weather.coord.lon == -0.1278
    assert weather.name == "London"


def test_get_current_weather_city_not_found(mock_requests_get):
    mock_response = Mock()
    mock_response.json.return_value = {"cod": 404}
    mock_requests_get.return_value = mock_response

    with pytest.raises(CityNotFound):
        get_current_weather("InvalidCity")


def test_get_current_weather_connection_error(mock_requests_get):
    mock_requests_get.side_effect = requests.ConnectionError

    with pytest.raises(ConnectionError):
        get_current_weather("London")


def test_check_weather_data_success():
    mock_response = Mock()
    mock_response.json.return_value = {
        "cod": "200",
        "cnt": 8,
        "list": [
            {
                "main": {"temp": 15.0, "feels_like": 14.0, "temp_min": 10.0, "temp_max": 20.0, "pressure": 1012, "humidity": 50},
                "weather": [{"main": "Clear", "description": "clear sky", "icon": "01d"}]
            } for _ in range(8)
        ]
    }

    time_data = check_weather_data(mock_response)
    assert len(time_data) == 8
    assert all(isinstance(td, TimeData) for td in time_data)


def test_check_weather_data_forecast_error():
    mock_response = Mock()
    mock_response.json.return_value = {"cod": "404"}

    with pytest.raises(ForecastError):
        check_weather_data(mock_response)


def test_get_weather_forecast_success(mock_requests_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "cod": "200",
        "cnt": 8,
        "list": [
            {
                "main": {"temp": 15.0, "feels_like": 14.0, "temp_min": 10.0, "temp_max": 20.0, "pressure": 1012, "humidity": 50},
                "weather": [{"main": "Clear", "description": "clear sky", "icon": "01d"}]
            } for _ in range(8)
        ]
    }
    mock_requests_get.return_value = mock_response

    forecasts = get_weather_forecast(51.5074, -0.1278)
    assert len(forecasts) == 8
    assert all(isinstance(td, TimeData) for td in forecasts)


def test_get_weather_forecast_connection_error(mock_requests_get):
    mock_requests_get.side_effect = requests.ConnectionError

    with pytest.raises(ConnectionError):
        get_weather_forecast(51.5074, -0.1278)


def test_get_start_utc_time():
    hours_back = 5
    expected_time = int((datetime.now(timezone.utc) - timedelta(hours=hours_back)).timestamp())
    assert get_start_utc_time(hours_back) == expected_time



def test_get_historical_data_success(mock_requests_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "cod": "200",
        "cnt": 8,
        "list": [
            {
                "main": {"temp": 15.0, "feels_like": 14.0, "temp_min": 10.0, "temp_max": 20.0, "pressure": 1012, "humidity": 50},
                "weather": [{"main": "Clear", "description": "clear sky", "icon": "01d"}]
            } for _ in range(8)
        ]
    }
    mock_requests_get.return_value = mock_response

    historical_data = get_historical_data(51.5074, -0.1278)
    assert len(historical_data) == 8
    assert all(isinstance(td, TimeData) for td in historical_data)


def test_get_historical_data_connection_error(mock_requests_get):
    mock_requests_get.side_effect = requests.ConnectionError

    with pytest.raises(ConnectionError):
        get_historical_data(51.5074, -0.1278)
