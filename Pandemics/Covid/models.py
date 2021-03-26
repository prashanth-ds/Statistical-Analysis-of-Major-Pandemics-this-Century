from django.db import models

# Create your models here.


class WorldDaily(models.Model):
    country_name = models.CharField(max_length=128)
    total_cases = models.CharField(max_length=12)
    new_cases = models.CharField(max_length=12)
    total_deaths = models.CharField(max_length=12)
    new_deaths = models.CharField(max_length=12)
    total_recovered = models.CharField(max_length=12)
    active_cases = models.CharField(max_length=12)
    population = models.CharField(max_length=50)
    latest_update = models.DateTimeField(auto_now=True)

    class Meta():
        db_table = 'covid_daily'

    def __str__(self):
        return self.country_name


class CovidWHO(models.Model):
    date_reported = models.CharField(max_length=25)
    country_code = models.CharField(max_length=7)
    country = models.CharField(max_length=128)
    who_region = models.CharField(max_length=7)
    new_cases = models.CharField(max_length=13)
    cumulative_cases = models.CharField(max_length=13)
    new_deaths = models.CharField(max_length=13)
    cumulative_deaths = models.CharField(max_length=13)

    class Meta():
        db_table = 'covid_world_who'

    def __str__(self):
        return self.country


class CovidIndia(models.Model):
    date = models.CharField(max_length=10)
    time = models.CharField(max_length=10)
    state_unionT = models.CharField(max_length=50)
    confirmed_indian = models.CharField(max_length=10)
    confirmed_foreign = models.CharField(max_length=10)
    cured = models.CharField(max_length=10)
    death = models.CharField(max_length=10)
    confirmed_total = models.CharField(max_length=10)

    class Meta():
        db_table = 'covid_india'

    def __str__(self):
        """
            note that whatever will be returned here will be used as foreign key referencing.
            i.e if self.time is returned self.time will be used as foreign key in other tables.
            :return self.date, will act as primary key, i.e anytime whatever self object is returned that will be pk
        """
        return self.date


class CovidIndiaTesting(models.Model):
    date_testing = models.CharField(max_length=13)
    state_unionT = models.CharField(max_length=50)
    total_samples = models.CharField(max_length=25)
    positive = models.CharField(max_length=25)
    negative = models.CharField(max_length=25)

    class Meta():
        db_table = 'covid_india_testing'

    def __str__(self):
        return self.state_unionT


class DataAutomation(models.Model):
    dates = models.DateField()
    who_country = models.IntegerField()
    indian_states = models.IntegerField()
    indian_states_testing = models.IntegerField()

    class Meta():
        db_table = 'data_automation'

    def __str__(self):
        return self.dates

