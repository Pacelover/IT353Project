from django.test import TestCase, Client
from django.urls import reverse
from weather import models

class TestButtonSubmit(TestCase):
    def setUp(self):
        self.client = Client()

    def test(self):
        self.client.post('', {'name': 'Chicago'})
        response = self.client.get(reverse('weather_data'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="Chicago"')

class TestAddCity(TestCase):
    def setUp(self):
        self.client = Client()

    def test(self):
        self.client.post('/weather/', {'city': 'Los Angeles'})
        response = self.client.get(reverse('add'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Los Angeles')

class TestDeleteCity(TestCase):

    def setUp(self):
        self.client = Client()
        models.City.objects.create(name="Chicago")
    
    def test(self):
        response = self.client.get(reverse('weather_delete'))
        print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Chicago')
