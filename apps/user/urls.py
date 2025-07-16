from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register(r'user', PersonalView, basename='auth')

urlpatterns = [
    path('register', RegisterView.as_view(), name='auth-register'),
    path('login', LoginView.as_view(), name='auth-login'),
    path('confirm-code', ConfirmCodeView.as_view(), name='auth-confirm-email'),
    path('re-send/email', ReSendView.as_view(), name='auth-re-send'),
    path('profile', UserProfileView.as_view(), name='auth-profile'),

    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/', include('allauth.socialaccount.urls')),

    path('', include(router.urls)),
]
