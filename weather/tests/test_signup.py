# import pytest
# from django.test import TestCase
# from django.urls import reverse
# from unittest.mock import patch
# from front.views import signup
#
# class SignUpViewTest(TestCase):
#     @patch('front.views.signup')
#     def test_signup_success(self, mock_signup):
#         # Mock the signup function to return a mocked response
#         mock_signup.return_value = 'mocked_response'
#
#         # Simulate a POST request with valid data
#         response = self.client.post(reverse('signup'),
#                                     {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpassword'})
#
#         # Assert that the signup function was called
#         mock_signup.assert_called_once_with({'username': 'testuser', 'email': 'test@example.com', 'password': 'testpassword'})
#
#         # Assert that the user was redirected to the index page
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, reverse('index'))