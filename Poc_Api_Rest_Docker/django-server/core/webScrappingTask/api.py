from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from core.webScrappingTask.models import Tarefas, Clientes, InformacaoAlvo
from core.webScrappingTask.serializers import TarefasSerializer, ClientesSerializer, InformacaoAlvoSerializer



class TarefasViewSet(viewsets.ModelViewSet):
    '''
    TarefasViewSet: Classes para exibicao do DataSet Serializado do Model Tarefas.
    '''
    queryset = Tarefas.objects.all()
    serializer_class = TarefasSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get"]

class ClientesViewSet(viewsets.ModelViewSet):
    '''
    ClientesViewSet: Classes para exibicao do DataSet Serializado do Model Clientes.
    '''
    queryset = Clientes.objects.all()
    serializer_class = ClientesSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get"]

class InformacaoAlvoViewSet(viewsets.ModelViewSet):
    '''
    InformacaoAlvoViewSet: Classes para exibicao do DataSet Serializado do Model InformacaoAlvo.
    '''
    queryset = InformacaoAlvo.objects.all()
    serializer_class = InformacaoAlvoSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get"]