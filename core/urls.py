
# from django.contrib import admin
# from django.urls import path, include
# from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('avia/', include('apps.tickets.urls')),  
#     path('base/', include('apps.main.urls')),
#     path('payment/', include('apps.payment.urls')),


#     path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
#     path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
# ]


from core import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions



schema_view = get_schema_view(
    openapi.Info(
        title="Concept.kg",
        default_version='v1',
        description="Документация Concenpt API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)



urlpatterns = [
    # documentation for API
    path('Concept/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # apps urls
    path('admin/', admin.site.urls),
    path('avia/', include('apps.tickets.urls')),
    path('user/', include('apps.user.urls')),  
    path('main/', include('apps.main.urls')),
    path('payment/', include('apps.payment.urls')),

    # DRF Spectacular
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)