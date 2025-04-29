
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),  # Админка Django
    path('', include('ads.urls')),    # Подключаем маршруты из приложения ads
    path('api/', include('ads.api')),  # Маршруты API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  # Схема OpenAPI
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # Swagger UI
]
