from django import forms
from core.webScrappingTask.models import InformacaoAlvo

class TargetInformationForm(forms.ModelForm):
    class Meta:
        model = InformacaoAlvo
        fields = ['url_alvo', 'codigo_acesso']
