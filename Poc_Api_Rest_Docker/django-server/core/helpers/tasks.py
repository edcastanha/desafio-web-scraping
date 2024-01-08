import pika
from django.conf import settings
from celery import shared_task
from core.helpers.loggingMe import logger
from django.utils import timezone
import requests

def get_queue(instance_id):
    """
    Envia o ID da instância InformacaoAlvo para uma fila RabbitMQ.

    Args:
    - instance_id: O ID da instância InformacaoAlvo a ser enviado para a fila.
    """
    try:
        # Conecta-se ao RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
        channel = connection.channel()

        # Declare a fila (caso ainda não exista)
        channel.queue_declare(queue='nome_da_fila')  # Substitua 'nome_da_fila' pelo nome desejado para a fila

        # Envia uma mensagem para a fila RabbitMQ com o ID da instância InformacaoAlvo
        channel.basic_publish(
            exchange='',
            routing_key='nome_da_fila',  # Substitua 'nome_da_fila' pelo nome desejado para a fila
            body=f'ID da instância InformacaoAlvo: {instance_id}',
        )

        # Fecha a conexão com o RabbitMQ
        connection.close()
    except Exception as e:
        # Lida com possíveis erros ao enviar para a fila RabbitMQ
        logger.error(f"Erro ao enviar para a fila RabbitMQ: {e}")

@shared_task(name="run_web_Scrapping_Task")
def run_webScrappingTask(task_instance):
    """
    Tarefa Celery para realizar scraping e enviar o ID da instância InformacaoAlvo para a fila RabbitMQ.

    Args:
    - task_instance: Instância da Tarefa associada à InformacaoAlvo.
    """
    try:
        logger.debug(f'Iniciando a tarefa de scrapping: {task_instance.id}')
        inicio = timezone.now()
        logger.debug(f'Tarefa de scrapping iniciada: {inicio}')
        
        data_info = task_instance.id_informacao_alvo.get_data
        
        # Chama a função para enviar para a fila RabbitMQ passando o ID da instância
        get_queue(task_instance.id)
        
        logger.debug(f'Mensagem enviada para a fila RabbitMQ')
    except requests.exceptions.RequestException as e:
        logger.error(f'Erro de solicitação: {e}')
