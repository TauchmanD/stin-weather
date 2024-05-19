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


@pytest.fixture
def mock_get_current_weather():
    with patch('front.data_handler.get_current_weather') as mock:
        yield mock


def test_get_query_weather_with_query(mock_get_current_weather):
    # Mocking the request object
    request = Mock()
    request.GET.get.return_value = 'London'

    # Mocking the response from get_current_weather function
    mock_get_current_weather.return_value = 'mocked_current_weather_data'

    # Call the function
    current_weather, error_message = get_query_weather(request)

    # Assertions
    assert current_weather == 'mocked_current_weather_data'
    assert error_message is None


def test_get_query_weather_no_query(mock_get_current_weather):
    # Mocking the request object
    request = Mock()
    request.GET.get.return_value = None

    # Mocking the response from get_current_weather function
    mock_get_current_weather.return_value = 'mocked_current_weather_data'

    # Call the function
    current_weather, error_message = get_query_weather(request)

    # Assertions
    assert current_weather == 'mocked_current_weather_data'
    assert error_message is None


def test_get_query_weather_city_not_found(mock_get_current_weather):
    # Mocking the request object
    request = Mock()
    request.GET.get.return_value = 'InvalidCity'

    # Mocking the exception raised by get_current_weather function
    mock_get_current_weather.side_effect = CityNotFound

    # Call the function
    current_weather, error_message = get_query_weather(request)

    # Assertions
    assert current_weather is None
    assert error_message == 'City not found'


def test_is_users_favourite_with_authenticated_user():
    # Mock current weather and request objects
    current_weather_mock = Mock()
    request_mock = Mock()

    # Set the user attribute of the request object
    request_mock.user.is_authenticated = True

    # Mock the filter method and its return value
    with patch('front.data_handler.FavouriteLocation.objects.filter') as mock_filter:
        mock_filter.return_value.exists.return_value = True

        # Call the function to be tested
        result = is_users_favourite(current_weather_mock, request_mock)

        # Assert that the filter method was called with the correct arguments
        mock_filter.assert_called_once_with(
            user=request_mock.user,
            latitude=current_weather_mock.coord.lat,
            longitude=current_weather_mock.coord.lon
        )

        # Assert that the function returns True
        assert result is True


def test_get_user_favorites_with_user():
    # Mock the user object
    user_mock = Mock()

    # Mock the filter method and its return value
    with patch('front.data_handler.FavouriteLocation.objects.filter') as mock_filter:
        mock_filter.return_value = ['favorite1', 'favorite2']

        # Call the function to be tested
        result = get_user_favorites(user_mock)

        # Assert that the filter method was called with the correct argument
        mock_filter.assert_called_once_with(user=user_mock)

        # Assert that the function returns the expected value
        assert result == ['favorite1', 'favorite2']


def test_get_user_favorites_without_user():
    # Mock the filter method
    with patch('front.data_handler.FavouriteLocation.objects.filter') as mock_filter:
        # Set the return value of the mock filter to an empty list
        mock_filter.return_value = []

        # Call the function to be tested
        result = get_user_favorites(None)

        # Assert that the filter method was called with the correct argument
        mock_filter.assert_called_once_with(user=None)

        # Assert that the function returns None
        assert result is None