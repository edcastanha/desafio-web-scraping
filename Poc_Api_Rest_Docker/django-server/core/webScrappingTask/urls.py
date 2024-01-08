from django.urls import path, include
from rest_framework import routers
from core.webScrappingTask.api import TarefasViewSet, InformacaoAlvoViewSet
from core.webScrappingTask.views import index, new_target

# Configuração das rotas da API usando DRF Router
router = routers.DefaultRouter()
router.register(r'tasks', TarefasViewSet, basename='tasks')
router.register(r'targets', InformacaoAlvoViewSet, basename='targets')

# Configuração das URLs da aplicação web
urlpatterns = [
    path('', index, name='index'),  # Rota para a view 'index' da aplicação web
    path('new_goal/', new_target, name='new_target'),  # Rota para a view 'new_target' da aplicação web
    path('api/', include(router.urls)),  # Incluindo as rotas da API usando o 'include'
    # outras URLs...
]
