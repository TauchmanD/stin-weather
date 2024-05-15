from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from front.data_handler import get_current_weather
from front.models import FavouriteLocation
from front.user_handling import register_user, authenticate_user
from front.errors import CityNotFound, EmptySearch
from front.decorators import payment_required

# Create your views here.


def index(request):
    error_message = None
    current_weather = None
    favorite = False
    query = request.GET.get('query')
    if query:
        try:
            current_weather = get_current_weather(query)
        except CityNotFound:
            error_message = 'City not found'
    else:
        current_weather = get_current_weather()

    if current_weather and request.user.is_authenticated:
        favorite = FavouriteLocation.objects.filter(
            user=request.user, latitude=current_weather.coord.lat,
            longitude=current_weather.coord.lon
        ).exists()

    if 'error' in request.session:
        error_message = request.session.pop('error')

    context = {
        "current_weather": current_weather,
        "weather": current_weather.weather[0] if current_weather else None,
        "image_path": "front/icons/" + current_weather.weather[0].icon + ".png" if current_weather else None,
        "coords": current_weather.coord if current_weather else None,
        "error_message": error_message,
        "favourite": favorite
    }
    return render(request, "front/index.html", context)


@login_required(login_url='login')
@payment_required(payment_url='payment')
def add_favorite(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        query = request.POST.get('query')
        favorite_location, created = FavouriteLocation.objects.get_or_create(
            user=request.user,
            latitude=latitude,
            longitude=longitude
        )
        if created:
            print("created favorite")
            favorite_location.save()
        else:
            print("already favorite")
    redirect_url = reverse('index')

    return HttpResponseRedirect(f'{redirect_url}?query={query}')


@login_required(login_url='login')
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


@login_required(login_url='signup')
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

