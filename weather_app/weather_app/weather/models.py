from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self): #see city chosen by user
        return self.name

    class Meta: # show cities instead of city when displaying more than 1
        verbose_name_plural = 'cities'