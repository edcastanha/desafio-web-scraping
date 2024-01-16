import requests
from django.conf import settings
from core.helpers.loggingMe import logger
from core.helpers.publisher import Publisher  
from django.core.serializers import serialize
from django.utils import timezone

publisher = Publisher(exchange='teste', queue_name='scrapping', routing_key='api-django')

def run_webScrappingTask(task_instance):
      """
    Tarefa envia a instância InformacaoAlvo para a fila.

    Args:
    - task_instance: Instância da Tarefa associada à InformacaoAlvo.
    """
    try:
        inicio = timezone.now()
        logger.debug(f'<:: Tasks - run_webScrappingTask:: Data = {task_instance} as {inicio}')

        # Adicione um log para verificar se a mensagem foi publicada com sucesso
        result = publisher.publish_message(task_instance, 'api-django')
        if result:
            logger.debug(f'<:: Tasks - run_webScrappingTask:: Publisher Queue - Message published successfully')
        else:
            logger.warning(f'<:: Tasks - run_webScrappingTask:: Publisher Queue - Message publication failed')

    except requests.exceptions.RequestException as e:
        error_message = f"Uma exceção do tipo {type(e).__name__} ocorreu com a mensagem: {str(e)}"
        logger.error(f'<:: Tasks - run_webScrappingTask:: Exception: {error_message}')
