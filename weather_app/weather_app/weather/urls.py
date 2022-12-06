from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='weather_data'),
    path('<int:weather_id>/delete', views.delete, name='delete'),
    path('<int:weather_id>/update', views.update, name='update'),
    path('add/', views.add, name='add')
]