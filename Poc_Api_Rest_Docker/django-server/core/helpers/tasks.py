from celery import shared_task
import requests
from core.helpers.loggingMe import logger
from django.utils import timezone

@shared_task(name="run_web_Scrapping_Task")
def run_webScrappingTask(task_instance):
    try:
        logger.debug(f'Iniciando a tarefa de scrapping: {task_instance.id}')
        inicio = timezone.now()
        logger.debug(f'Tarefa de scrapping iniciada: {inicio}')
        
        data_info = task_instance.id_informacao_alvo.get_data
        
        logger.debug(f'Resposta da API: {response}')
    except requests.exceptions.RequestException as e:
        logger.error(f'Erro de solicitação: {e}')

