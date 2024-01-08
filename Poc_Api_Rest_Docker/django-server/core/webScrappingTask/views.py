from rest_framework.decorators import api_view
from django.middleware.csrf import get_token
from django.shortcuts import render
from core.webScrappingTask.models import InformacaoAlvo
from core.webScrappingTask.serializers import InformacaoAlvoSerializer

# Frontend
def index(request):
    # Obtém o token CSRF
    key = {}
    key['csrf_token'] = get_token(request)
    return render(request, "index.html", key)

# Rota para criar um novo registro de InformacaoAlvo
@api_view(['POST'])
def new_target(request):
    try:
        token = request.data.get('token')
        url_alvo = request.data.get('url_alvo')
        codigo_acesso = request.data.get('codigo_acesso')

        if any(v is None or v == '' for v in (token, url_alvo, codigo_acesso)):
            return Response({'mensagem': 'Dados insuficientes para criar InformacaoAlvo'}, status=status.HTTP_400_BAD_REQUEST)

        informacao_alvo = InformacaoAlvo.objects.filter(token=token).first()
        if informacao_alvo:
            return Response({'mensagem': 'Token já existe'}, status=status.HTTP_400_BAD_REQUEST)

        nova_informacao_alvo = InformacaoAlvo.objects.create(
            token=token,
            url_alvo=url_alvo,
            codigo_acesso=codigo_acesso,
        )

        return Response({'mensagem': 'Nova InformacaoAlvo criada com sucesso!'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'mensagem': 'Ocorreu um erro: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
