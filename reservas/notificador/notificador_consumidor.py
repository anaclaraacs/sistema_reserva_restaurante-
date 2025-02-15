import pika
from time import sleep
import logging

RABBITMQ_HOST = "rabbitmq"
QUEUE_NAME = "reservas"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def callback(ch, method, properties, body):
    mensagem = body.decode("utf-8")
    logger.info(f"📩 Mensagem recebida: {mensagem}")
    # Aqui você pode adicionar a lógica para enviar notificações


print(RABBITMQ_HOST)

while True:
    try:
        conexao = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        if conexao:
            break
    except Exception as e:
        logger.error(e)

canal = conexao.channel()
canal.queue_declare(queue=QUEUE_NAME)

logger.info("🎧 Consumidor RabbitMQ rodando...")
canal.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)

canal.start_consuming()
