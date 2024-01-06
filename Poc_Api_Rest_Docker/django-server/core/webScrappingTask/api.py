from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from core.webScrappingTask.models import Tarefas
from core.webScrappingTask.serializers import TarefasSerializer

class TarefasViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Tarefas.objects.all()
    serializer_class = TarefasSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get"]