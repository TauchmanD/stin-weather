from django.test import TestCase, RequestFactory
from unittest.mock import patch
from front.views import index
from front.models import CurrentWeather, Weather, WeatherInfo, Location


class IndexViewTest(TestCase):
    @patch("front.views.get_current_weather")
    def test_index_view(self, mock_get_current_weather):
        expected_current_weather = CurrentWeather(
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

        mock_get_current_weather.return_value = expected_current_weather

        request = RequestFactory().get("/")
        response = index(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            expected_current_weather.weather[0].main, response.content.decode("utf-8")
        )
        self.assertIn(
            str(expected_current_weather.main.temp), response.content.decode("utf-8")
        )
