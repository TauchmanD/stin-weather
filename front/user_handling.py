from django.db import IntegrityError

from django.contrib.auth.hashers import make_password
from .models import WeatherUser


def authenticate_user(email, password):
    try:
        user = WeatherUser.objects.get(email=email)
        if user.check_password(password):
            return user
    except WeatherUser.DoesNotExist:
        return None


def register_user(username, email, password):
    try:
        hashed_password = make_password(password)
        user = WeatherUser(username=username, email=email, password=hashed_password)
        user.save()
        return user
    except IntegrityError:
        return None
