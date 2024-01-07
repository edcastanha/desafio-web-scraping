# Para criar as visualizacoes.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required # É necessário iniciar sessão para aceder a páginas privadas
from django.views.decorators.cache import cache_control # # É necessário iniciar sessão para aceder a páginas privadas

#Utils function Django

from django.http import JsonResponse

# ======== Models ========
from core.webScrappingTask.models import Tarefas, Clientes, InformacaoAlvo



# ============ JSON ============
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def tarefas_json(request):
    objs = Tarefas.objects.all()
    data = [obj.get_data() for obj in objs]
    response = {'data':data}
    return JsonResponse(response)