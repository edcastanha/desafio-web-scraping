import pika
import json
import time
from datetime import datetime as dt
from helpers.logging_me import logger
from helpers.configuration import Configuration
from helpers.scrapping import Jobs
from helpers.conectionDB import DatabaseConnection

class ConsumerExtractor:
    '''
    Classe que representa o consumidor de mensagens do RabbitMQ para execução de tarefas relacionadas ao Jobs.

    Responsabilidades:
    - Estabelecer conexão com o RabbitMQ.
    - Processar mensagens recebidas.
    - Executar tarefas associadas aos Jobs com base nas mensagens.
    - Registrar status e atualizar dados no banco de dados.

    Métodos:
    - __init__: Inicializa as variáveis e objetos necessários para conexão e processamento.
    - connect_to_rabbitmq: Estabelece a conexão com o RabbitMQ.
    - run: Executa o consumidor para receber e processar mensagens.
    - process_message: Processa as mensagens recebidas do RabbitMQ.
    '''

    def __init__(self):
        # Inicializa as variáveis para controle de conexão
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 3
        self.reconnecting = False
        self.connection = None
        self.channel = None
        self.db_connection = DatabaseConnection()

    def connect_to_rabbitmq(self):
        '''
        Estabelece a conexão com o RabbitMQ.
        '''
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
            # Configurações de bind e consumo de mensagens
            # ...
        except Exception as e:
            # Tratamento de erros ao estabelecer a conexão
            # ...

    def run(self):
        '''
        Executa o consumidor para receber e processar mensagens.
        '''
        logger.debug('<*_ConsumerExtractor_*> Run - Init')
        try:
            # Lógica principal para execução do consumidor
            # ...
        except KeyboardInterrupt:
            # Tratamento de interrupção de teclado
            # ...
        except Exception as e:
            # Tratamento de exceções durante a execução
            # ...
        finally:
            # Operações de limpeza ao final da execução
            # ...

    def process_message(self, ch, method, properties, body):
        '''
        Processa as mensagens recebidas do RabbitMQ.
        '''
        # Lógica de processamento das mensagens
        # ...

if __name__ == "__main__":
    job = ConsumerExtractor()
    job.run()
