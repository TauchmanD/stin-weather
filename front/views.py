from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from front.data_handler import get_current_weather

# Create your views here.


def index(request):
    current_weather = get_current_weather(47.46, 7.38)
    context = {
        'current_weather': current_weather,
        'weather': current_weather.weather[0],
        'image_path': "front/icons/" + current_weather.weather[0].icon + ".png"
    }
    return render(request, 'front/index.html', context)
