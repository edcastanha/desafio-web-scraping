from django.urls import include, path
from rest_framework import routers
from core.webScrappingTask.api import TarefasViewSet, InformacaoAlvoViewSet

# URLS API
router = routers.DefaultRouter()
router.register(r'tasks', TarefasViewSet, basename='tasks')
router.register(r'targets', InformacaoAlvoViewSet, basename='targets')

# WEB APP
from core.webScrappingTask import views

urlpatterns = [
    # WEB APP
    path('', views.index, name="index"),

]

