from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

#URLs API
from rest_framework import routers
from core.webScrappingTask.urls import router as webScrappingTask_router

#URLs ADMIN e SITE
from django.contrib import admin
from core.webScrappingTask import urls as app_urls

# URLs DE API
router = routers.DefaultRouter()
router.registry.extend(webScrappingTask_router.registry)

# URLS DE ADMIN e SITE
urlpatterns = [
    path('', include(app_urls)),  # WEB
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),  # ADMIN
]

#Adicione as rotas para os arquivos estáticos e de mídia apenas em ambiente de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)