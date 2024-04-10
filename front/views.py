from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from front.data_handler import get_current_weather

# Create your views here.


def index(request):
    current_weather = get_current_weather(50.77, 15.05)
    return JsonResponse(current_weather.json(), safe=False)
