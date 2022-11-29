from django.test import TestCase, Client
from django.urls import reverse

class TestButtonSubmit(TestCase):
    def setUp(self):
        self.client = Client()

    def test(self):
        self.client.post('', {'name': 'Chicago'})
        response = self.client.get(reverse('weather_data'))
        self.assertEqual(response.status_code, 200)
        print(response)
        #self.assertEqual(response, 'Chicago')
