from django.urls import path

from core.webScrappingTask.viewsets import WebScrapingViewSet

urlpatterns = [
    path('v1/scrapping/', WebScrapingViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('v1/scrapping/<int:pk>/', WebScrapingViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'})),
]