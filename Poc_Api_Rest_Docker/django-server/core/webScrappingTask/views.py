from django.middleware.csrf import get_token
from django.shortcuts import render
from core.webScrappingTask.forms import TargetInformationForm
from core.helpers.loggingMe import logger

# === Frontend ===
def index(request):
    if request.method == 'POST':
        form = TargetInformationForm(request.POST)
        if form.is_valid():
            novo_alvo = form.save()  # Salvar o objeto InformacaoAlvo
            logger.info(f"TargetInformationForm:: {novo_alvo}")
    else:
        form = TargetInformationForm()
    
    return render(request, 'index.html', {'form': form})


