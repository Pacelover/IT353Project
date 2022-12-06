from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=25)
    # created_at = models.DateTimeField('Created', auto_now_add=True)
    # update_at = models.DateTimeField('Updated', auto_now=True)
    # isCompleted = models.BooleanField(default=False)

    def __str__(self): #see city chosen by user
        return self.name