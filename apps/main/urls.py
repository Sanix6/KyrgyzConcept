from django.urls import path
from apps.main import views 

urlpatterns = [
    path('search/params', views.CountryAirportListView.as_view(), name='country-airport-list'),
]