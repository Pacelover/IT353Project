from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=25)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self): #see city chosen by user
        return self.name

    def setName(self, aName):
        self.name = aName
    
    def printName(self):
        print(self.name)
    class Meta: #show the plural of city as cities instead of citys
        verbose_name_plural = 'cities'

