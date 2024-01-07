from django.urls import include, path
from rest_framework import routers
from core.webScrappingTask.api import TarefasViewSet, InformacaoAlvoViewSet

# URLS API
router = routers.DefaultRouter()
router.register(r'tarefas', TarefasViewSet, basename='tarefas')
router.register(r'alvos', InformacaoAlvoViewSet, basename='alvos')

# WEB APP
from core.webScrappingTask import views

urlpatterns = [
    # WEB APP
    path('', views.index, name="index"),
    path('novaTarefa', views.nova_tarefa, name='nova_tarefa'),

    # JSON
    path('tarefas/json', views.tarefas_json, name="tarefas_json"),
]

