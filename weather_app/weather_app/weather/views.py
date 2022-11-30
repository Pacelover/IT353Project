from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
from django.contrib.gis.geoip2 import GeoIP2

# Create your views here.
def index(request):
    # API
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=60191ca9e0dc4470867884ba38fd64d8'
    # cities = City.objects.all() # return all cities in db
    cityName = 'Normal'

    try:
        #get location from ip
        #src https://stackoverflow.com/questions/2218093/django-retrieve-ip-location 
        g = GeoIP2()
        ip = request.META.get('REMOTE_ADDR', None)
        if ip:
            cityName = g.city(ip)
    except:
        pass
        
    if request.method == 'POST':
        form = CityForm(request.POST)
        cityName = request.POST['name']
        form.save
    form = CityForm()
    # Request API data and convert to json type
    city = requests.get(url.format(cityName)).json()
    try:
        lon = city['coord']['lon']
        lat = city['coord']['lat']
        # print(city)
        url = 'http://api.openweathermap.org/geo/1.0/reverse?lat={}&lon={}&limit=5&appid=60191ca9e0dc4470867884ba38fd64d8'
        location = requests.get(url.format(lat, lon)).json()
        state = location[0]['state']
        print("Location: ", state)
        # dictionary that stores weather data retrieved by user
        weather = {
            'city': city['name'] + ', ' + state,
            'temperature': city['main']['temp'],
            'description': city['weather'][0]['description'],
            'icon': city['weather'][0]['icon'],
            'feels like': city['main']['feels_like'],
            'humidity': city['main']['humidity']
        }
    except:
        print("City not found")
        weather = {
            'city': '',
            'state': '',
            'temperature': '',
            'description': '',
            'icon': ''
        }
    #print(weather)
    context = {'weather': weather, 'form': form}
    return render(request, 'weather/index.html', context) # returns the index.html template
