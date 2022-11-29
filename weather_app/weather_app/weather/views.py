from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):
    # API
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=60191ca9e0dc4470867884ba38fd64d8'
    # cities = City.objects.all() # return all cities in db
    cityName = 'Normal'
    if request.method == 'POST':
        form = CityForm(request.POST)
        cityName = request.POST['name']
        form.save
    form = CityForm()
    # Request API data and convert to json type
    city = requests.get(url.format(cityName)).json()
    #print(city)
    # dictionary that stores weather data retrieved by user
    weather = {
        'city': city['name'],
        'temperature': city['main']['temp'],
        'description': city['weather'][0]['description'],
        'icon': city['weather'][0]['icon']
    }
    context = {'weather': weather, 'form': form}
    #print(weather)
    return render(request, 'weather/index.html', context) # returns the index.html template