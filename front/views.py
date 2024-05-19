from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from front.data_handler import get_query_weather, is_users_favourite, get_user_favorites, get_weather_forecast, get_historical_data
from front.models import FavouriteLocation
from front.user_handling import register_user, authenticate_user
from front.errors import CityNotFound, EmptySearch
from front.decorators import payment_required
from weather import settings


# Create your views here.


def index(request):
    current_weather, error_message = get_query_weather(request)
    favorite = is_users_favourite(current_weather, request)

    context = {
        "current_weather": current_weather,
        "weather": current_weather.weather[0] if current_weather else None,
        "image_path": "front/icons/" + current_weather.weather[0].icon + ".png" if current_weather else None,
        "coords": current_weather.coord if current_weather else None,
        "error_message": error_message,
        "favourite": favorite
    }
    return render(request, "front/index.html", context)


@login_required(login_url='signin')
@payment_required(payment_url='payment')
def favourites(request):
    favourites_list = get_user_favorites(request.user)
    context = {
        "favourites": favourites_list,
        "key": settings.USER_API_KEY
    }
    return render(request, 'front/favourites.html', context)


@login_required(login_url='signin')
@payment_required(payment_url='payment')
def location_detail(request):
    lat = request.GET.get('latitude')
    lon = request.GET.get('longitude')
    name = request.GET.get('name')

    forecast = get_weather_forecast(lat, lon)
    history = get_historical_data(lat, lon)

    context = {
        "name": name,
        "latitude": lat,
        "longitude": lon,
        "forecast": forecast,
        "history": history
    }

    return render(request, "front/location_detail.html", context)


@login_required(login_url='signin')
@payment_required(payment_url='payment')
def add_favorite(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        query = request.POST.get('query')
        favorite_location, created = FavouriteLocation.objects.get_or_create(
            user=request.user,
            latitude=latitude,
            longitude=longitude,
            name=query
        )
        if created:
            print("created favorite")
            favorite_location.save()
        else:
            print("already favorite")
    redirect_url = reverse('index')

    return HttpResponseRedirect(f'{redirect_url}?query={query}')


@login_required(login_url='signin')
@payment_required(payment_url='payment')
def remove_favorite(request):
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')
    query = request.POST.get('query')

    favorite_location = FavouriteLocation.objects.get(user=request.user, latitude=latitude, longitude=longitude)
    favorite_location.delete()
    redirect_url = reverse('index')

    return HttpResponseRedirect(f'{redirect_url}?query={query}')


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        user = register_user(username, email, password)
        if user:
            login(request, user)
            return redirect('index')
        return render(request, 'front/signup.html', {'error': 'Email already used'})
    return render(request, 'front/signup.html')


def signin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate_user(email, password)
        if user:
            print(user)
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'front/login.html', {'error': 'Invalid username or password'})
    return render(request, 'front/login.html')


def signout(request):
    logout(request)
    return redirect('index')


@login_required(login_url='signin')
def payment(request):
    if request.method == "POST":
        card_number = request.POST.get("card_number")
        expiration_date = request.POST.get("expiration_date")
        cvv = request.POST.get("cvv")

        if card_number and expiration_date and cvv:
            user = request.user
            user.paying = True
            user.save()
            return redirect('index')
        return render(request, 'front/payment.html', {'error': 'Invalid card info'})
    return render(request, 'front/payment.html')

