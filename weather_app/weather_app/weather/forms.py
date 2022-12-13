from django.forms import ModelForm, TextInput
from .models import City

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name', 'author']
        widgets = {
            'name': TextInput(attrs={'class': 'input', 'placeholder': 'City Name'})
        } #update input class to use the CSS properly