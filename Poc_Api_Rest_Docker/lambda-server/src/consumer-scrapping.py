import pika
import json
import time
from datetime import datetime as dt
from helpers.logging_me import logger
from helpers.configuration import Configuration
from helpers.scrapping import Jobs

class ConsumerExtractor:
    def __init__(self):
        # Inicializa as variáveis para controle de conexão
        self.reconnect_attempts = 0  # Contagem de tentativas de reconexão
        self.max_reconnect_attempts = 3  # Limite de tentativas de reconexão
        self.reconnecting = False  # Flag para indicar se está reconectando
        self.connection = None  # Objeto de conexão com o RabbitMQ
        self.channel = None  # Objeto de canal do RabbitMQ
        self.db_connection = DatabaseConnection()  # Objeto de conexão com o banco de dados

    def connect_to_rabbitmq(self):
        try:
            # Estabelece a conexão com o RabbitMQ
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=Configuration.RMQ_SERVER,
                    port=Configuration.RMQ_PORT,
                    credentials=pika.PlainCredentials(
                        Configuration.RMQ_USER,
                        Configuration.RMQ_PASS),
                        heartbeat=6000
                    )
                )
            self.channel = self.connection.channel()
            self.channel.queue_bind(
                queue=Configuration.RMQ_QUEUE_PUBLISHIR,
                exchange=Configuration.RMQ_EXCHANGE,
                routing_key=Configuration.RMQ_ROUTE_KEY
            )
            self.channel.basic_consume(
                queue=Configuration.RMQ_QUEUE_CONSUMER,
                on_message_callback=self.process_message,
            )
            
            self.reconnect_attempts = 0  # Reinicia a contagem após uma conexão bem-sucedida
            self.reconnecting = False  # Define como falso após uma conexão bem-sucedida
        except Exception as e:
            error_message = f"Erro de conexão ao RabbitMQ: {str(e)}"
            logger.error(f'<*_ConsumerExtractor_*> Connection Error: {error_message}')
            self.reconnecting = True  # Indica que está tentando reconectar
  
    def run(self):
        logger.debug('<*_ConsumerExtractor_*> Run - Init')
        try:
            if not self.reconnecting:
                self.connect_to_rabbitmq()  # Conecta-se ao RabbitMQ se não estiver reconectando

            self.channel.start_consuming()  # Inicia o consumo de mensagens
        except KeyboardInterrupt:
            self.channel.stop_consuming()  # Encerra o consumo de mensagens em caso de interrupção do teclado
        except Exception as e:
            # Em caso de exceção, tenta reconectar-se dentro do limite de tentativas
            error_message = f"Uma exceção do tipo {type(e).__name__} ocorreu com a mensagem: {str(e)}"
            logger.error(f'<*_ConsumerExtractor_*> Exception-Run: {error_message}')
            self.reconnect_attempts += 1
            if self.reconnect_attempts <= self.max_reconnect_attempts:
                time.sleep(2)
        finally:
            # Fecha a conexão com o banco de dados ao final
            if self.db_connection.is_connected():
                self.db_connection.close()
            logger.debug('<*_ConsumerExtractor_*> Run - Finally :')

    def process_message(self, ch, method, properties, body):
        # Processa a mensagem recebida do RabbitMQ
        data = json.loads(body)
        id_procesamento = int(data['id'])
        url = data['url']
        code = data['codigo']
        self.db_connection.connect()
        try:
            # Executa tarefas associadas ao Jobs
            task = Jobs(url, code)
            task.scrape()
            logger.info(f'<*_ConsumerExtractor_*> Process_Message - Iniciado')
            now = dt.now()
            values = (now, now, )
            self.db_connection.update(Configuration.UPDATE_QUERY, ('Finalizado', id_procesamento))
            self.db_connection.insert(Configuration.INSER_QUERY, values)
            logger.info(f'<*_ConsumerExtractor_*> Execucoes SQL com dados:: {values}')         
        except Exception as e:
            # Em caso de exceção, registra o erro e confirma a entrega da mensagem
            self.db_connection.update(Configuration.UPDATE_QUERY, ('Error', id_procesamento))
            error_message = f"Uma exceção do tipo {type(e).__name__} ocorreu com a mensagem: {str(e)}"
            logger.error(f'<*_ConsumerExtractor_*> Process_Message: {error_message}')
            self.channel.basic_ack(method.delivery_tag)
        finally:
            self.channel.basic_ack(method.delivery_tag)
            # Atualiza o status do processamento e registra a finalização do processamento da mensagem
            self.db_connection.update(Configuration.UPDATE_QUERY, ('Finalizado', id_procesamento))
            logger.info(f'<*_ConsumerExtractor_*> Process_Message - Finish')
         
if __name__ == "__main__":
    job = ConsumerExtractor()
    job.run()
