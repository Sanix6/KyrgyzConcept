from django.urls import path
from apps.tickets import views

urlpatterns = [
    path('search-flights/', views.SearchFlightsView.as_view()), 
    path('get-schedule/', views.GetScheduleView.as_view()),
    path('create-order/', views.CreateOrderView.as_view()),
    path('order/payment/', views.OrderPaymentView.as_view()),
    path('order/cancel/<str:order_id>', views.CancelOrderView.as_view()),
    path('order/status/', views.OrderStatusView.as_view()),
    path('order/info/<str:order_id>', views.GetOrderInfoView.as_view()),
    path('get-offers/', views.GetOffersView.as_view()),
    path('check-offer-avail/<str:buy_id>', views.CheckOfferAvailiblityView.as_view()),
]
