from django.urls import path
from . import views

app_name = 'H1N1'

urlpatterns = [
    path('', views.EachCountry.as_view(), name='h1n1_list'),
]
