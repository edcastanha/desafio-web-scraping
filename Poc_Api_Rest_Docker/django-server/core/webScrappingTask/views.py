# Para criar as visualizacoes.
from django.template.context_processors import csrf
from django.shortcuts import render
from django.contrib.auth.decorators import login_required # É necessário iniciar sessão para aceder a páginas privadas
from django.views.decorators.cache import cache_control # # É necessário iniciar sessão para aceder a páginas privadas

#Utils function
from django.http import JsonResponse
from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from core.webScrappingTask.models import Tarefas,  InformacaoAlvo

# Frontend
def index(request):
    # Obtém o token CSRF
    key = {}
    key.update(csrf(request))
    return render(request, "index.html")


@api_view(['POST'])
def nova_tarefa(request):
    # Extrair os dados recebidos na solicitação POST
    key = request.data.get('token')
    url_alvo = request.data.get('url_alvo')
    codigo_acesso = request.data.get('codigo_acesso')

    # Verificar se todos os dados necessários foram recebidos
    if url_alvo is None or codigo_acesso is None:
        return Response({'mensagem': 'Dados insuficientes para criar InformacaoAlvo'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Criar um novo objeto InformacaoAlvo com base nos dados recebidos
        nova_informacao_alvo = InformacaoAlvo.objects.create(
            token=key,
            url_alvo=url_alvo,
            codigo_acesso=codigo_acesso,
        )

        # Salvar o novo objeto no banco de dados
        nova_informacao_alvo.save()

        # Retornar uma resposta para indicar o sucesso da criação
        return Response({'mensagem': 'Nova Tarefa Alvo criada com sucesso!'}, status=status.HTTP_201_CREATED)
    except IntegrityError as e:
        # Lidar com a exceção de integridade (por exemplo, chave duplicada)
        return Response({'mensagem': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # Se ocorrer um erro, retorne uma resposta com o erro específico para identificação
        return Response({'mensagem': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# ============ JSON ============
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def tarefas_json(request):
    objs = Tarefas.objects.all()
    data = [obj.get_data() for obj in objs]
    response = {'data':data}
    return JsonResponse(response)
