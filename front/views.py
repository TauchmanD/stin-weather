from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from front.data_handler import get_current_weather, get_lat_long_from_search
from front.user_handling import register_user, authenticate_user
from front.errors import CityNotFound, EmptySearch

# Create your views here.


def index(request, lat=None, lon=None):
    error_message = None
    if lat is not None and lon is not None:
        current_weather = get_current_weather(lat, lon)
    else:
        current_weather = get_current_weather()

    if 'error' in request.session:
        error_message = request.session.pop('error')

    context = {
        "current_weather": current_weather,
        "weather": current_weather.weather[0] if current_weather else None,
        "image_path": "front/icons/" + current_weather.weather[0].icon + ".png" if current_weather else None,
        "error_message": error_message
    }
    print(error_message)
    return render(request, "front/index.html", context)

def search_location(request):
    search_string = request.GET.get('search_string', '')
    if search_string:
        try:
            location = get_lat_long_from_search(search_string)
            return redirect('index_with_coordinates', lat=location.lat, lon=location.lon)
        except CityNotFound:
            request.session['error'] = 'City not found'
    return redirect('index')



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

