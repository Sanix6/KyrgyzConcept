from django.urls import path
from apps.tickets import views

urlpatterns = [
    path('search-flights/', views.SearchFlightsView.as_view()), 
    path('get-schedule/', views.GetScheduleView.as_view()),
    path('create-order/', views.CreateOrderView.as_view()),
    path('order/payment/', views.OrderPaymentView.as_view()),
    path('order/cancel/', views.CancelOrderView.as_view()),
    path('order/payment-status/', views.OrderStatusView.as_view()),
    path('order/info', views.GetOrderInfoView.as_view()),
]
