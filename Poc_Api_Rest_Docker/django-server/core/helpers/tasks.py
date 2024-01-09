import pika
import json 
import requests
from django.conf import settings
from core.helpers.loggingMe import logger
from core.helpers.publisher import Publisher  
from django.core.serializers import serialize
from django.utils import timezone

# Objeto da classe Publisher
publisher = Publisher(exchange='teste', queue_name='scrapping', routing_key='proccess')

def run_webScrappingTask(task_instance):
    """
    Tarefa envia a instância InformacaoAlvo para a fila.

    Args:
    - task_instance: Instância da Tarefa associada à InformacaoAlvo.
    """
    try:
        inicio = timezone.now()
        logger.debug(f'<:: Tasks - run_webScrappingTask::{task_instance.id} as {inicio}')
        
        # Serializa a instância para um formato que pode ser transmitido
        serialized_instance = serialize('json', [task_instance])

        # Converte o dicionário em JSON
        serialized_instance = json.dumps(serialized_instance)

        # Publica a mensagem na fila RabbitMQ com a instância serializada usando o objeto da classe Publisher
        publisher.publish_message(serialized_instance)  # Passa a instância serializada como mensagem
        
        logger.debug(f'<:: Tasks - run_webScrappingTask:: Publisher Queue')
    except requests.exceptions.RequestException as e:
        logger.error(f'<:: Tasks - run_webScrappingTask:: Exception: {e}')