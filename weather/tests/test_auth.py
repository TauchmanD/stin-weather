import pytest
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import AbstractBaseUser
from unittest.mock import patch

from front.models import WeatherUser
from front.user_handling import authenticate_user, register_user


@pytest.fixture
def mock_user():
    return WeatherUser(
        username='testuser',
        email='test@example.com',
        password=make_password('testpassword')
    )


def test_authenticate_user_success(mocker, mock_user):
    mock_get = mocker.patch('front.models.WeatherUser.objects.get')
    mock_get.return_value = mock_user

    authenticated_user = authenticate_user(mock_user.email, 'testpassword')
    assert authenticated_user is not None
    assert authenticated_user.email == mock_user.email


def test_authenticate_user_wrong_password(mocker, mock_user):
    mock_get = mocker.patch('front.models.WeatherUser.objects.get')
    mock_get.return_value = mock_user

    authenticated_user = authenticate_user(mock_user.email, 'wrongpassword')
    assert authenticated_user is None


def test_authenticate_user_user_does_not_exist(mocker):
    mock_get = mocker.patch('front.models.WeatherUser.objects.get', side_effect=WeatherUser.DoesNotExist)

    authenticated_user = authenticate_user('nonexistent@example.com', 'testpassword')
    assert authenticated_user is None
