from django.urls import path
from .views import (
    MKassaLoginView,
    MKassaCreatePaymentView,
    MKassaCheckPaymentView,
    MkassaCallbackView,
)

urlpatterns = [
    path('login/', MKassaLoginView.as_view(), name='mkassa-login'),
    path('create-payment/', MKassaCreatePaymentView.as_view(), name='mkassa-create-payment'),
    path('check-payment/<str:payment_id>/', MKassaCheckPaymentView.as_view(), name='mkassa-check-payment'),
    path('callback/', MkassaCallbackView.as_view(), name='mkassa-callback'),
]
