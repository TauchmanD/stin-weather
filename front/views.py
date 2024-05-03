from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

from front.data_handler import get_current_weather
from front.user_handling import register_user, authenticate_user

# Create your views here.


def index(request):
    print(request.user)
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
