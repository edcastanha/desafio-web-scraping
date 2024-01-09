import pika
from core.helpers.loggingMe import logger
from core.settings import RBMQ_HOST, RBMQ_PORT, RBMQ_USER, RBMQ_PASS

class Publisher:
    """
    Classe responsável por publicar mensagens em filas de mensageria (RabbitMQ para o exemplo do WebScrapping).

    Args:
    - exchange (str): Nome da exchange.
    - queue_name (str): Nome da fila a ser verificada/criada.
    - routing_key (str): Chave de roteamento para a mensagem.
    """
    def __init__(self, exchange, queue_name, routing_key):
        self.exchange = exchange
        self.queue_name = queue_name
        self.routing_key = routing_key
        self.connection = self._establish_connection()
        self.properties = pika.BasicProperties(delivery_mode=2)
        self.channel = self.connection.channel()

        self.create_or_get_queue()
        self.create_or_get_queue_success()

    def _establish_connection(self):
        """
        Estabelece a conexão com o servidor RabbitMQ.

        Returns:
        - connection: Objeto de conexão com o RabbitMQ.
        """
        return pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RBMQ_HOST,
                port=RBMQ_PORT,
                credentials=pika.PlainCredentials(RBMQ_USER, RBMQ_PASS)
            )
        )

    def create_or_get_queue(self, routing_key = 'proccess'):
        """
        Verifica se a fila especificada existe no RabbitMQ.
        Caso não exista, a fila é criada.
        """
        try:
            # Cria a exchange se não existir
            self.channel.exchange_declare(exchange=self.exchange, exchange_type='direct')

            # Cria a fila se não existir
            self.channel.queue_declare(queue=self.queue_name, durable=True)

            # Faz o bind da fila à exchange
            self.channel.queue_bind(
                exchange=self.exchange,
                queue=self.queue_name,
                routing_key=self.routing_key
            )

            logger.info(f'Exchange e fila verificadas/criadas com sucesso')
        except Exception as e:
            logger.error(f'Erro ao verificar/criar exchange e fila: {str(e)}')
            self.close()

    def create_or_get_queue_success(self, routing_key = 'update'):
            """
            Verifica se a fila especificada existe no RabbitMQ.
            Caso não exista, a fila é criada.
            """
            try:
                # Cria a exchange se não existir
                self.channel.exchange_declare(exchange=self.exchange, exchange_type='direct')

                # Cria a fila se não existir
                self.channel.queue_declare(queue='success', durable=True)

                # Faz o bind da fila à exchange
                self.channel.queue_bind(
                    exchange=self.exchange,
                    queue='success',
                    routing_key=self.routing_key
                )
                logger.info(f'Exchange e fila verificadas/criadas com sucesso')
            except Exception as e:
                logger.error(f'Erro ao verificar/criar exchange e fila: {str(e)}')
                self.close()


    def publish_message(self, message, routing_key=None):
        """
        Publica uma mensagem na fila especificada.

        Args:
        - message (str): Mensagem a ser publicada.
        - routing_key (str, opcional): Chave de roteamento para a mensagem. Se não for especificada, utiliza a routing_key definida na inicialização.
        """
        if routing_key is None:
            routing_key = self.routing_key

        logger.info(f'<**_Publicando na Fila_**> ROUTER_KEY:: {routing_key}')
        try:
            self.channel.basic_publish(
                exchange=self.exchange,
                routing_key=routing_key,
                body=message,
                properties=self.properties
            )
        except Exception as e:
            logger.error(f'<**_Core_Publisher_**> Erro ao Publicar: {str(e)}')
            self.close()

    def bind_queue(self, routing_key=None):
        """
        Realiza o bind da fila à exchange com a routing_key especificada ou a routing_key padrão.

        Args:
        - routing_key (str, opcional): Chave de roteamento para a bind. Se não for especificada, utiliza a routing_key definida na inicialização.
        """
        if routing_key is None:
            routing_key = self.routing_key

        logger.info(f'<**_Ligando na Fila_**> ROUTER_KEY:: {routing_key}')
        try:
            self.channel.queue_bind(
                queue=self.queue_name,
                exchange=self.exchange,
                routing_key=routing_key
            )
        except Exception as e:
            logger.error(f'<**_Core_Publisher_**> Erro ao fazer bind na fila: {str(e)}')
            self.close()

    def close(self):
        """
        Fecha a conexão com o RabbitMQ.
        """
        if self.channel.is_open:
            self.channel.close()
            logger.info(f'<**_Core_Publisher_**> Fechando Canal Comunicacao')
