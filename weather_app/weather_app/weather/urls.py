from django.urls import include, path
from . import views

app_name='weather'
urlpatterns = [
    path('', views.index, name='weather_data'),
    path('add/', views.add, name='add'),
    path(r'^delete/(?P<pk>[0-9]+)/$', views.delete, name='weather_delete'),
    path('accounts/', include('django.contrib.auth.urls'))
]