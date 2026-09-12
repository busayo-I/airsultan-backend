from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from django.conf.urls.static import static
from django.conf import settings

def api_root(request):
    return JsonResponse({
        'message': 'Welcome to AirSultan API',
        'docs'   : 'http://127.0.0.1:8000/api/docs/',
        'admin'  : 'http://127.0.0.1:8000/admin/',
        'version': 'v1.0.0',
    })

urlpatterns = [
    path('',             api_root),
    path('admin/',       admin.site.urls),

    # API routes
    path('api/admin/auth/', include('accounts.urls')),
    path('api/admin/offers/', include('offers.urls')),
    path('api/admin/insights/', include('insights.urls')),
    path('api/admin/travel-requests/', include('travel_requests.urls')),

    # Swagger documentation
    path('api/schema/',  SpectacularAPIView.as_view(),                        name='schema'),
    path('api/docs/',    SpectacularSwaggerView.as_view(url_name='schema'),   name='swagger-ui'),
    path('api/redoc/',   SpectacularRedocView.as_view(url_name='schema'),     name='redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)