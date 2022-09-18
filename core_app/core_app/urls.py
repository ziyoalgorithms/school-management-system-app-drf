from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),

    # API dokumentatsiya urllari
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs',
    ),
    # O'qituvchi va talabalar urli (staffs app urls)
    path('staffs/', include('staffs.urls')),
    # Dars urllari (lesson app urls)
    path('lesson/', include('lesson.urls')),
    # To'lov urllari (payment app urls)
    path('payment/', include('payment.urls'))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )