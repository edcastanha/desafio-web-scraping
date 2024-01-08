from helpers.loggingMe import logger
import pika

def callback(ch, method, properties, body):
    print("Mensagem recebida:", body)

connection = pika.BlockingConnection(pika.ConnectionParameters('broker-server'))
channel = connection.channel()

channel.queue_declare(queue='fila_exemplo')

channel.basic_consume(queue='fila_exemplo', on_message_callback=callback, auto_ack=True)

print('Aguardando mensagens. Para sair, pressione CTRL+C')
channel.start_consuming()
