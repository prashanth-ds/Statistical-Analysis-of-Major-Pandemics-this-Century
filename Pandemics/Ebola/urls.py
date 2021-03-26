from django.urls import path
from . import views

app_name = 'Ebola'

urlpatterns = [
    path('', views.EachCountry.as_view(), name='ebola_list'),
]