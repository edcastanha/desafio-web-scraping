from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.response import Response
from core.webScrappingTask.models import Tarefas, InformacaoAlvo
from core.webScrappingTask.serializers import TarefasSerializer, InformacaoAlvoSerializer

class TarefasViewSet(viewsets.ModelViewSet):
    '''
    TarefasViewSet: Classes para exibicao do DataSet Serializado do Model Tarefas.
    '''
    queryset = Tarefas.objects.all()
    serializer_class = TarefasSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get"]

class InformacaoAlvoViewSet(viewsets.ModelViewSet):
    '''
    InformacaoAlvoViewSet: Classes para exibicao do DataSet Serializado do Model InformacaoAlvo.
    '''
    queryset = InformacaoAlvo.objects.all()
    serializer_class = InformacaoAlvoSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
