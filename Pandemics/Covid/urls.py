from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name = 'Covid'
urlpatterns = [
    path('', views.TempView.as_view(), name='world_list'),
    path('<int:pk>', views.EachCountryDetails.as_view(), name='world_detail'),
    path('India/', views.IndianStates.as_view(), name='india_list'),
    path('India/<int:pk>', views.IndiaDetails.as_view(), name='india_detail'),
]
urlpatterns += staticfiles_urlpatterns()
