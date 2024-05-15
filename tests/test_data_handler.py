import pytest
import requests

from unittest.mock import patch
from front.models import CurrentWeather, Weather, WeatherInfo, Location, Coords
from front.data_handler import get_current_weather


@patch("requests.get")
def test_get_current_weather_success(mock_get):
    mock_response = {
        "coord": {"lon": 42, "lat": 57},
        "weather": [
            {"id": 801, "main": "Clouds", "description": "few clouds", "icon": "02d"}
        ],
        "base": "stations",
        "main": {
            "temp": 8.26,
            "feels_like": 5.09,
            "temp_min": 8.26,
            "temp_max": 8.26,
            "pressure": 993,
            "humidity": 58,
            "sea_level": 993,
            "grnd_level": 979,
        },
        "visibility": 10000,
        "wind": {"speed": 5.84, "deg": 238, "gust": 9.35},
        "clouds": {"all": 18},
        "dt": 1713191887,
        "sys": {"country": "RU", "sunrise": 1713146584, "sunset": 1713198027},
        "timezone": 10800,
        "id": 533555,
        "name": "Lukh",
        "cod": 200,
    }

    mock_get.return_value.json.return_value = mock_response

    query = "Lukh"
    current_weather = get_current_weather(query)

    expected_current_weather = CurrentWeather(
        coord=Coords(lat=57, lon=42),
        weather=[Weather(main="Clouds", description="few clouds", icon="02d")],
        main=WeatherInfo(
            temp=8.26,
            feels_like=5.09,
            temp_min=8.26,
            temp_max=8.26,
            pressure=993.0,
            humidity=58.0,
        ),
        sys=Location(country="RU", sunrise=1713146584, sunset=1713198027),
        timezone=10800,
        name="Lukh",
    )

    assert current_weather == expected_current_weather


@patch("requests.get")
def test_get_current_weather_connection_error(mock_get):
    mock_get.side_effect = requests.ConnectionError()

    with pytest.raises(ConnectionError):
        get_current_weather("Liberec")
