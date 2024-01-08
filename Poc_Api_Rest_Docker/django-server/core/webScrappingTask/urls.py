from django.urls import path
from core.webScrappingTask.views import index, new_goal

# Configuração das URLs da aplicação web
urlpatterns = [
    path('', index, name='index'),
    path('new_goal/', new_goal, name='new_goal'),
]
