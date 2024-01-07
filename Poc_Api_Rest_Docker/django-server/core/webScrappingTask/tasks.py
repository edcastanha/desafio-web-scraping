from celery import shared_task
import requests
from core.loggingMe import logger
from django.utils import timezone

@shared_task(name="run_web_Scrapping_Task")
def run_webScrappingTask(task_instance):
    
    if _check_task_date(task_instance):
        try:
            api_url = "http://localhost:5000/scrapping"
            data_info = task_instance.id_informacao_alvo.get_data
            response = requests.post(api_url, data={'action': 'created', 'body': task_instance})
            logger.debug(f'Resposta da API: {response}')
        except requests.exceptions.RequestException as e:
            logger.error(f'Erro de solicitação: {e}')

