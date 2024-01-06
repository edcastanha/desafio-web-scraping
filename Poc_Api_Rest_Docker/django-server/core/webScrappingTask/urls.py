from django.urls import include, path
from rest_framework import routers
from core.webScrappingTask.api import TarefasViewSet
router = routers.DefaultRouter()
router.register(r'tarefas', TarefasViewSet, basename='tarefas')

from core.cadastros import views 

urlpatterns = [
    # API REST
    path('tarefas/', include(router.urls)),

    # Frontend
    path('listar_tarefas/', views.listar_tarefas, name="listar_tarefas"),
    
    # JSON
    path('tarefas/json/', views.tarefas_json, name="tarefas_json"),
]