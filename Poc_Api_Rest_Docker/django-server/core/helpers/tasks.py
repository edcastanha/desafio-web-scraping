import pika
from django.conf import settings
from core.helpers.loggingMe import logger
from core.helpers.publisher import Publisher  
from django.core.serializers import serialize
from django.utils import timezone
import requests

# Objeto da classe Publisher
publisher = Publisher(exchange='teste', queue_name='scrapping', routing_key='tasks')

def run_webScrappingTask(task_instance):
    """
    Tarefa Celery para realizar scraping e enviar a instância InformacaoAlvo para a fila RabbitMQ.

    Args:
    - task_instance: Instância da Tarefa associada à InformacaoAlvo.
    """
    try:
        logger.debug(f'Iniciando a tarefa de scrapping: {task_instance.id}')
        inicio = timezone.now()
        logger.debug(f'Tarefa de scrapping iniciada: {inicio}')
        
        # Serializa a instância para um formato que pode ser transmitido
        serialized_instance = serialize('json', [task_instance])

        # Publica a mensagem na fila RabbitMQ com a instância serializada usando o objeto da classe Publisher
        publisher.publish_message(serialized_instance)  # Passa a instância serializada como mensagem
        
        logger.debug(f'Mensagem enviada para a fila RabbitMQ')
    except requests.exceptions.RequestException as e:
        logger.error(f'Erro de solicitação: {e}')
