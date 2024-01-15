from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from core.webScrappingTask.models import TargetSiteData
from core.webScrappingTask.serializers import TargetSiteDataSerializer

class WebScrapingViewSet(viewsets.ViewSet):
    def get_queryset(self):
        return TargetSiteData.objects.all()

    def list(self, request):
        items = self.get_queryset()
        serializer = TargetSiteDataSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(TargetSiteData, pk=pk)
        serializer = TargetSiteDataSerializer(item)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = TargetSiteDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        item = get_object_or_404(TargetSiteData, pk=pk)
        serializer = TargetSiteDataSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
