from django.urls import path
from apps.tickets import views

urlpatterns = [
    path('search-flights/', views.SearchFlightsView.as_view()), 
    path('get-schedule/', views.GetScheduleView.as_view()),
    path('etm-login/', views.EtmLoginView.as_view()),
    path('create-order/', views.CreateOrderView.as_view()),
]
