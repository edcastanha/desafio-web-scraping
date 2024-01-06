from rest_framework import serializers
from core.webScrappingTask.models import Tarefas


class TarefasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarefas
        fields = '__all__'