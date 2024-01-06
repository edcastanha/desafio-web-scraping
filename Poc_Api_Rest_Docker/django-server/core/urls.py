from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
#URLs API
from rest_framework import routers
from core.webScrappingTask.urls import router

#URLs ADMIN e SITE
from django.contrib import admin
from core.webScrappingTask import urls as app_urls

# URLs DE API
router = routers.DefaultRouter()
router.registry.extend(router.registry)

# URLS DE ADMIN e SITE
urlpatterns = [
    path('admin/', admin.site.urls),  # ADMIN
    path('api/v1/', include(router.urls)),  # API REST
    path('', include(app_urls)),  # SITE
]

# INCLUDES static e media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)