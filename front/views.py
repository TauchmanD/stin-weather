from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from front.data_handler import get_current_weather
from front.user_handling import register_user, authenticate_user

# Create your views here.


def index(request):
    current_weather = get_current_weather(57.00, 42.00)
    context = {
        "current_weather": current_weather,
        "weather": current_weather.weather[0],
        "image_path": "front/icons/" + current_weather.weather[0].icon + ".png",
    }
    return render(request, "front/index.html", context)


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

