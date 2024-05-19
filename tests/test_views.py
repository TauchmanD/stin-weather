import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client
from unittest.mock import patch
from front.models import FavouriteLocation

User = get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

@pytest.fixture
def client():
    return Client()

@patch('front.data_handler.get_query_weather')
@patch('front.data_handler.is_users_favourite')
def test_index_view(mock_is_users_favourite, mock_get_query_weather, client):
    mock_get_query_weather.return_value = (None, None)
    mock_is_users_favourite.return_value = False

    response = client.get(reverse('index'))
    assert response.status_code == 200
    assert 'front/index.html' in [t.name for t in response.templates]


def test_location_detail(client):
    # Make a request to the location_detail view without authentication
    response = client.get(reverse('location_detail') + '?latitude=0&longitude=0&name=Test', follow=True)

    # Assert that the response redirects to the login page
    assert response.status_code == 200


