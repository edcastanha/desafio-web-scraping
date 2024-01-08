import pika
import json
import time
from datetime import datetime as dt
from helpers.logging_me import logger
from helpers.configuration import Configuration
from helpers.scrapping import Jobs

class ConsumerExtractor:
    def __init__(self):
        self.reconnect_attempts = 0  # Adicione uma contagem de tentativas de reconexão
        self.max_reconnect_attempts = 3  # Defina um limite de tentativas de reconexão
        self.reconnecting = False
        self.connection = None
        self.channel = None
        self.publisher = Push()
        self.db_connection = DatabaseConnection()

    def connect_to_rabbitmq(self):
        try:
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
                queue = Configuration.RMQ_QUEUE_PUBLISHIR,
                exchange = Configuration.RMQ_EXCHANGE,
                routing_key = Configuration.RMQ_ROUTE_KEY
            )
            self.channel.basic_consume(
                queue = Configuration.RMQ_QUEUE_CONSUMER,
                on_message_callback = self.process_message,
            )
            
            self.reconnect_attempts = 0  # Redefina a contagem de tentativas após uma conexão bem-sucedida
            self.reconnecting = False
        except Exception as e:
            error_message = f"Erro de conexão ao RabbitMQ: {str(e)}"
            logger.error(f'<*_ConsumerExtractor_*> Connection Error: {error_message}')
            self.reconnecting = True
  
    def run(self):
            logger.debug('<*_ConsumerExtractor_*> Run - Init')
            try:
                if not self.reconnecting:
                    self.connect_to_rabbitmq()

                self.channel.start_consuming()
            except KeyboardInterrupt:
                self.channel.stop_consuming()
            except Exception as e:
                error_message = f"Uma exceção do tipo {type(e).__name__} ocorreu com a mensagem: {str(e)}"
                logger.error(f'<*_ConsumerExtractor_*> Exception-Run: {error_message}')
                self.reconnect_attempts += 1
                if self.reconnect_attempts <= self.max_reconnect_attempts:
                    time.sleep(2)
            finally:
                #Postgres Connection
                if self.db_connection.is_connected():
                    self.db_connection.close()
                    #logger.debug('<*_ConsumerExtractor_*> Run - DB Connection Close')
                logger.debug('<*_ConsumerExtractor_*> Run - Finally :')

    def process_message(self, ch, method, properties, body):
        data = json.loads(body)
        id_procesamento = int(data['id'])
        url = data['url']
        code = data['codigo']
        self.db_connection.connect()
        try:
            task = Jobs(url, code)
            task.scrape()
            logger.info(f'<*_ConsumerExtractor_*> Process_Message - Iniciado')
            now = dt.now()
            values =  (now, now, )
            self.db_connection.update(Configuration.UPDATE_QUERY, ('Finalizado', id_procesamento))
            self.db_connection.insert(Configuration.INSER_QUERY, values)
            logger.info(f'<*_ConsumerExtractor_*> Execucoes SQL com dados:: {values}')         
        except Exception as e:
            self.db_connection.update(Configuration.UPDATE_QUERY, ('Error', id_procesamento))
            error_message = f"Uma exceção do tipo {type(e).__name__} ocorreu com a mensagem: {str(e)}"
            logger.error(f'<*_ConsumerExtractor_*> Process_Message: {error_message}')
            #self.channel.basic_nack(method.delivery_tag, requeue=True) 
            #                 self.channel.basic_ack(method.delivery_tag)
            self.channel.basic_ack(method.delivery_tag)
        finally:
            self.channel.basic_ack(method.delivery_tag)
            # Update Status Processamento -  Processado devido nao haver faces
            self.db_connection.update(Configuration.UPDATE_QUERY, ('Finalizado', id_procesamento))
            logger.info(f'<*_ConsumerExtractor_*> Process_Message - Finish')
         
if __name__ == "__main__":
    job = ConsumerExtractor()
    job.run()
