from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm
from . import match_clothing
import geoip2.database
from django.views import generic
from django.http import HttpResponseRedirect

# Create your views here.
def index(request,localle_escape=False):
    # API
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=60191ca9e0dc4470867884ba38fd64d8'
    # cities = City.objects.all() # return all cities in db
    cityName = 'Normal'
    form = None
    cur_url = 'weather_data'

    cities = City.objects.all() 
    city_data = []
    for city in cities:
        city_data.append(city)
        print(city)
    print("City data" ,city_data)
    if not localle_escape:
        try:
            # get location from ip
            # src https://stackoverflow.com/questions/2218093/django-retrieve-ip-location 
            g = geoip2.database.Reader('../../geoip/GeoLite2-City.mmdb')
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            ip = None
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            if ip:
                if ip=='127.0.0.1':
                    print("Can't find a location from a localhost, dummy")
                    cityName = g.city('69.174.155.10')
                else:
                    cityName = g.city(ip)
                    print("Successfully acquired location from IP")
            
        except:
            pass
        
        if request.method == 'POST':
            form = CityForm(request.POST)
            cityName = request.POST.get('name', False)
            form.save
        if request.method == 'GET':
            print('Gotten')
            print(request.GET.get('name', False))
            form = CityForm(request.GET)
            cityName = request.GET.get('name', False)
            if cityName == False:
                cityName = 'Normal'
            form.save
            # redirect('weather:weather_data')
        form = CityForm()
    # Request API data and convert to json type
    city = requests.get(url.format(cityName)).json()
    clothStr = None
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
        # weather = {
        #     'city': 'DEFAULT',
        #     'state': 'DEFAULT',
        #     'temperature': '70',
        #     'description': 'DEFAULT',
        #     'icon': 'DEFAULT',
        #     'feels like':'70',
        #     'humidity':'50'
        # }
        # clothStr = ''
        return index(request,localle_escape=True)
        
    context = {'weather': weather, 'form': form,'cloth':clothStr, 'city_data': city_data, 'pname':cur_url}
    return render(request, 'weather/index.html', context) # returns the index.html template

def add(request):
    # city_data = []

    # cityName = request.POST.get('add', False)
    # cities = City.objects.create(cityName)

    # for city in cities:
    #     city_data.append(city)
    #     print(city_data)
    # item = City.objects.create()

    # item.setName('Chicago')
    # item.printName()

    form = CityForm(request.POST)
    form.save()


    return redirect('weather:weather_data')

    #return redirect('weather:add') OR return render(request, 'weather/index.html', context) however, you need to figure out what context will be equal to
    # OR you might not need to return or redirect anything since it's on the same page. We probably just need to refresh the page

def delete(request):
    item = City.objects.get()
    City.objects.delete(item)