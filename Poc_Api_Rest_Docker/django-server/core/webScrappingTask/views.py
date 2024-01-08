from rest_framework.decorators import api_view
from django.middleware.csrf import get_token
from django.shortcuts import render
from rest_framework import status
from django.http import JsonResponse
from rest_framework.response import Response

#from django.views.decorators.csrf import csrf_exempt

from core.webScrappingTask.serializers import InformacaoAlvoSerializer
from core.webScrappingTask.models import InformacaoAlvo

import json
from django.core.exceptions import ObjectDoesNotExist

# === Frontend ===
def index(request):
    key = {}
    key['csrf_token'] = get_token(request)
    return render(request, "index.html", key)

@api_view(['GET', 'POST'])
def informacao_alvo_view(request):
    if request.method == 'GET':
        try:
            informacoes = InformacaoAlvo.objects.all()
            serializer = InformacaoAlvoSerializer(informacoes, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'POST':
        payload = json.loads(request.body)
        try:
            target = InformacaoAlvo.objects.create(
                token=payload["token"],
                url_alvo=payload["url"],
                codigo_acesso=payload["codigo"],
            )
            serializer = InformacaoAlvoSerializer(target)
            return JsonResponse({'target': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ==== API ====
@api_view(['POST'])
def new_target(request):
    payload = json.loads(request.body)
    try:
        target = InformacaoAlvo.objects.create(
            token=payload["token"],
            url_alvo=payload["url"],
            codigo_acesso=payload["codigo"],
        )
        serializer = BookSerializer(book)
        return JsonResponse({'target': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
     
