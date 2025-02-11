import pika
from time import sleep

#sleep(10)
RABBITMQ_HOST = "rabbitmq"
QUEUE_NAME = "reservas"

def callback(ch, method, properties, body):
    mensagem = body.decode("utf-8")
    print(f"📩 Mensagem recebida: {mensagem}")
    # Aqui você pode adicionar a lógica para enviar notificações

print(RABBITMQ_HOST)
sleep(20)
conexao = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
canal = conexao.channel()
canal.queue_declare(queue=QUEUE_NAME)

print("🎧 Consumidor RabbitMQ rodando...")
canal.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)

canal.start_consuming()