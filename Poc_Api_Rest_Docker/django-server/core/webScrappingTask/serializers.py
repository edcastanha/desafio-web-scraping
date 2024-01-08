from rest_framework import serializers
from core.webScrappingTask.models import Tarefas, InformacaoAlvo


class TarefasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarefas
        fields = '__all__'


class InformacaoAlvoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformacaoAlvo
        fields = '__all__'