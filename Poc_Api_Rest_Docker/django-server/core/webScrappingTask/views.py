from django.shortcuts import render
from core.helpers.loggingMe import logger
from core.webScrappingTask.forms import TargetInformationForm
from core.webScrappingTask.models import InformacaoAlvo


def index(request):
    if request.method == 'POST':
        form = TargetInformationForm(request.POST)
        if form.is_valid():
            novo_alvo = form.save(commit=False)  # Não salve no banco de dados ainda
            token_csrf = request.POST.get('csrfmiddlewaretoken')  # Obtém o csrf_token do POST
            novo_alvo.token = token_csrf  # Atribui o csrf_token ao campo token
            
            novo_alvo.save()  # Salva o objeto InformacaoAlvo com o csrf_token
            
            id_salvo = novo_alvo.id
            token_salvo = novo_alvo.token
            
            # Agora você pode retornar esses dados para o template
            return render(request, 'index.html', {'form': form, 'token_salvo': token_salvo, 'id_salvo': id_salvo})
    else:
        form = TargetInformationForm()
    
    return render(request, 'index.html', {'form': form})
