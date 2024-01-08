from django.urls import path, include  # Adicionando 'include'
from rest_framework import routers
from core.webScrappingTask.api import TarefasViewSet, InformacaoAlvoViewSet
from core.webScrappingTask.views import index, new_target  # Importando as views corretamente

# URLS API
router = routers.DefaultRouter()
router.register(r'tasks', TarefasViewSet, basename='tasks')
router.register(r'targets', InformacaoAlvoViewSet, basename='targets')

# WEB APP
urlpatterns = [
    path('', index, name='index'),
    path('api/new_goal/', new_target, name='new_target'),  # Corrigindo o caminho da nova meta
    path('api/', include(router.urls)),  # Adicionando as rotas da API
    # outras URLs...
]
