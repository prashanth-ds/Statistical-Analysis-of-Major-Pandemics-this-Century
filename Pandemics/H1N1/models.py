from django.db import models

# Create your models here.


class WorldH1N1(models.Model):
    country = models.CharField(max_length=50)
    confirmed_cases = models.IntegerField()
    confirmed_deaths = models.IntegerField()

    class Meta():
        db_table = 'H1N1_World'

    def __str__(self):
        return self.country
