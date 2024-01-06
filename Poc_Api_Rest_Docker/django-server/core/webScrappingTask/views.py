# Para criar as visualizacoes.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required # É necessário iniciar sessão para aceder a páginas privadas
from django.views.decorators.cache import cache_control # # É necessário iniciar sessão para aceder a páginas privadas

# ======== Models ========
from core.webScrappingTask.models import Tarefas, Cliente, InformacaoAlvo

# ======== Frontend ========
# Listar Pessoas
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def listar_tarefas(request):
    return render(request, 'app/pages/listar-tarefas.html')
