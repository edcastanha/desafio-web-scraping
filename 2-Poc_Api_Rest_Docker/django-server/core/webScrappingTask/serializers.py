from rest_framework import serializers
from core.webScrappingTask.models import TargetSiteData

class TargetSiteDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetSiteData
        
        fields = '__all__'