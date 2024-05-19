# from unittest.mock import patch, MagicMock
#
# import pytest
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import AnonymousUser
# from django.test import RequestFactory
# from django.urls import reverse
# from front.models import WeatherUser, WeatherInfo, TimeData, Weather, CurrentWeather, \
#     Coords, FavouriteLocation  # Import the custom user model
# from front.views import index, favourites, add_favorite, remove_favorite, payment
#
# User = get_user_model()
#
# @pytest.fixture
# def request_factory():
#     return RequestFactory()
#
# @pytest.fixture
# def user():
#     return User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
#
#
# @pytest.fixture
# def paying_user():
#     return User.objects.create_user(username='testuser', email='test@example.com', password='testpassword', paying=True)
#
# @pytest.fixture
# def unauthenticated_user():
#     return AnonymousUser()
#
# @pytest.mark.django_db
# def test_index_view_authenticated_user(request_factory, user):
#     request = request_factory.get('/')
#     request.user = user
#     with patch('front.views.get_query_weather') as mock_get_query_weather:
#         mock_get_query_weather.return_value = (None, None)
#         response = index(request)
#         assert response.status_code == 200
#
#
# @pytest.mark.django_db
# def test_index_view_unauthenticated_user(request_factory, unauthenticated_user):
#     request = request_factory.get('/')
#     request.user = unauthenticated_user
#     response = index(request)
#     assert response.status_code == 200
#
#
# @pytest.mark.django_db
# def test_favourites_view_authenticated_user(request_factory, user):
#     request = request_factory.get('/favourites/')
#     request.user = user
#     with patch('front.views.get_user_favorites') as mock_get_user_favorites:
#         mock_get_user_favorites.return_value = []
#         response = favourites(request)
#         assert response.status_code == 302
#
#
# @pytest.mark.django_db
# def test_favourites_view(client, paying_user):
#     # Create a mock request
#     request = RequestFactory().get(reverse('favourites'))
#     request.user = paying_user  # Assign the paying user to the request
#
#     # Mock get_user_favorites function
#     with patch('front.views.get_user_favorites') as mock_get_user_favorites:
#         # Define the return value of the mock function
#         mock_favourites_list = ['Favorite1', 'Favorite2']
#         mock_get_user_favorites.return_value = mock_favourites_list
#
#         # Call the view function
#         response = favourites(request)
#
#     # Assertions
#     assert response.status_code == 200
#
#
# @pytest.mark.django_db
# def test_add_favorite_view(client, paying_user):
#     # Create a mock request
#     request = RequestFactory().post(reverse('add_favorite'), {'latitude': '51.5074', 'longitude': '-0.1278', 'query': 'London'})
#     request.user = paying_user  # Assign the paying user to the request
#
#     # Call the view function
#     response = add_favorite(request)
#
#     # Assertions
#     assert response.status_code == 302  # Redirect status code
#     assert response.url == reverse('index') + '?query=London'  # Verify redirection URL
#
#     # Verify that the FavouriteLocation object is created
#     assert FavouriteLocation.objects.filter(user=paying_user, latitude=51.5074, longitude=-0.1278, name='London').exists()
#
#
# @pytest.mark.django_db
# def test_remove_favorite_view(client, paying_user):
#     # Create a FavouriteLocation object for the user
#     FavouriteLocation.objects.create(user=paying_user, latitude=51.5074, longitude=-0.1278, name='London')
#
#     # Create a mock POST request to remove the favorite
#     request = RequestFactory().post(reverse('remove_favorite'), {'latitude': '51.5074', 'longitude': '-0.1278', 'query': 'London'})
#     request.user = paying_user  # Assign the paying user to the request
#
#     # Call the view function
#     response = remove_favorite(request)
#
#     # Assertions
#     assert response.status_code == 302  # Redirect status code
#     assert response.url == reverse('index') + '?query=London'  # Verify redirection URL
#
#     # Verify that the FavouriteLocation object is deleted
#     assert not FavouriteLocation.objects.filter(user=paying_user, latitude=51.5074, longitude=-0.1278, name='London').exists()
#
#
# @pytest.mark.django_db
# def test_payment_view(client, paying_user):
#     # Create a mock POST request with valid card information
#     request = RequestFactory().post(reverse('payment'), {'card_number': '1234567890123456', 'expiration_date': '01/23', 'cvv': '123'})
#     request.user = paying_user  # Assign the paying user to the request
#
#     # Call the view function
#     response = payment(request)
#
#     # Assertions
#     assert response.status_code == 302  # Redirect status code
#     assert response.url == reverse('index')  # Verify redirection URL
#
#     # Verify that the paying status of the user is updated
#     assert WeatherUser.objects.get(username=paying_user.username).paying == True