from django.db import models

# Create your models here.


class WorldEBola(models.Model):
    country = models.CharField(max_length=50)
    confirmed_cases = models.IntegerField()
    confirmed_deaths = models.IntegerField()


    class Meta():
        db_table = 'ebola_world'

    def __str__(self):
        return self.country
