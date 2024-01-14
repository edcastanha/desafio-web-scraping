from django.urls import path
from core.webScrappingTask.views import index


urlpatterns = [
    path('', index, name='index'),
]
