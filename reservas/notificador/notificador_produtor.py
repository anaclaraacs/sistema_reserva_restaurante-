import pika

RABBITMQ_HOST = "rabbitmq"
QUEUE_NAME = "reservas"

def enviar_mensagem(reserva_id, cliente_email):
    mensagem = f"Reserva {reserva_id} confirmada para {cliente_email}"

    conexao = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    canal = conexao.channel()
    canal.queue_declare(queue=QUEUE_NAME)

    canal.basic_publish(exchange='', routing_key=QUEUE_NAME, body=mensagem.encode("utf-8"))
    
    conexao.close()
    print(f"📩 Mensagem enviada para RabbitMQ: {mensagem}")