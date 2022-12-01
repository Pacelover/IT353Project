from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
from . import match_clothing

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
        clothStr = match_clothing.get_clothing(weather.get('temperature'), 'F', weather.get('feels like'), weather.get('humidity'))
    except:
        print("City not found")
        weather = {
            'city': '',
            'state': '',
            'temperature': '',
            'description': '',
            'icon': ''
        }
        clothStr = ''
    #print(weather)
    context = {'weather': weather, 'form': form,'cloth':clothStr}
    return render(request, 'weather/index.html', context) # returns the index.html template
