from django.shortcuts import render
import requests

# Create your views here.
def index(request):
    # API
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=60191ca9e0dc4470867884ba38fd64d8'
    city = 'Las Vegas'
    # Request API data and convert to json type
    city_weather = requests.get(url.format(city)).json()
    print(city_weather)
    return render(request, 'weather/index.html') # returns the index.html template