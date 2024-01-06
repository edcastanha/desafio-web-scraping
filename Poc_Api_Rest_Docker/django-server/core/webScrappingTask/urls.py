from django.urls import include, path
from rest_framework import routers
from core.webScrappingTask.api import TarefasViewSet
router = routers.DefaultRouter()
router.register(r'tarefas', TarefasViewSet, basename='tarefas')

from core.webScrappingTask import views 

urlpatterns = [
    # Frontend
    path('', views.index, name="index"),
    path('listar_tarefas/', views.listar_tarefas, name="listar_tarefas"),
    
    # Login/Logout
    path('login/', include('django.contrib.auth.urls')),

    # Backend
    path('backend/', views.backend, name="backend"),
    path('frequencia/<int:id>/', views.frequencia_view, name='frequencia'),

    # API REST
    path('tarefas/', include(router.urls)),

    # JSON
    path('tarefas/json/', views.tarefas_json, name="tarefas_json"),
]

