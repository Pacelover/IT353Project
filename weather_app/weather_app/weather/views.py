from django.shortcuts import render
import requests
from .models import City

# Create your views here.
def index(request):
    # API
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=60191ca9e0dc4470867884ba38fd64d8'
    cities = City.objects.all() # return all cities in db
    weather_data = []
    for city in cities:
        # Request API data and convert to json type
        city_weather = requests.get(url.format(city)).json()
        print(city_weather)
        # dictionary that stores weather data retrieved by user
        weather = {
            'city': city,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
        }
        weather_data.append(weather)
    context = {'weather_data': weather_data}
    print(weather)
    return render(request, 'weather/index.html', context) # returns the index.html template