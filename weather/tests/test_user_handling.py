import pytest
from unittest.mock import patch, Mock
from django.contrib.auth.hashers import make_password
from django.db.utils import IntegrityError
from front.user_handling import register_user, WeatherUser

@pytest.fixture
def mocked_make_password():
    with patch('front.user_handling.make_password') as mock_make_password:
        yield mock_make_password

@pytest.fixture
def mocked_weather_user():
    with patch('front.user_handling.WeatherUser') as mock_weather_user:
        yield mock_weather_user

def test_register_user_success(mocked_make_password, mocked_weather_user):
    # Arrange
    username = 'test_user'
    email = 'test@example.com'
    password = 'test_password'
    mocked_make_password.return_value = 'hashed_password'
    mocked_user_instance = Mock()
    mocked_weather_user.return_value = mocked_user_instance

    # Act
    result = register_user(username, email, password)

    # Assert
    assert result == mocked_user_instance
    mocked_make_password.assert_called_once_with(password)
    mocked_weather_user.assert_called_once_with(username=username, email=email, password='hashed_password')
    mocked_user_instance.save.assert_called_once()

def test_register_user_integrity_error(mocked_make_password, mocked_weather_user):
    # Arrange
    username = 'test_user'
    email = 'test@example.com'
    password = 'test_password'
    mocked_make_password.return_value = 'hashed_password'
    mocked_weather_user.side_effect = IntegrityError

    # Act
    result = register_user(username, email, password)

    # Assert
    assert result is None