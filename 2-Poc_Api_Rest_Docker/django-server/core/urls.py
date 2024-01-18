from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
from core.webScrappingTask import urls as api_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)