from rest_framework import serializers
from core.webScrappingTask.models import Tarefas, Clientes, InformacaoAlvo


class TarefasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarefas
        fields = '__all__'


class ClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientes
        fields = '__all__'


class InformacaoAlvoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformacaoAlvo
        fields = '__all__'