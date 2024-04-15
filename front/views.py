from django.shortcuts import render

from front.data_handler import get_current_weather

# Create your views here.


def index(request):
    current_weather = get_current_weather(57.00, 42.00)
    context = {
        "current_weather": current_weather,
        "weather": current_weather.weather[0],
        "image_path": "front/icons/" + current_weather.weather[0].icon + ".png",
    }
    return render(request, "front/index.html", context)
