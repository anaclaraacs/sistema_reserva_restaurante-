import pika
import json

RABBITMQ_HOST = "127.0.0.1" 
QUEUE_NAME = "reservas"

def enviar_mensagem(mesa_id, cliente_email):
    mensagem = {
        "mesa_id": mesa_id,
        "email_cliente": cliente_email
    }

    conexao = None 
    try:
        conexao = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        canal = conexao.channel()
        canal.queue_declare(queue=QUEUE_NAME)

        canal.basic_publish(exchange='', routing_key=QUEUE_NAME, body=json.dumps(mensagem).encode("utf-8"))
        print(f"Mensagem enviada para RabbitMQ: {mensagem}")
    except Exception as e:
        print(f"Erro ao enviar mensagem para RabbitMQ: {e}")
    finally:
        if conexao and not conexao.is_closed:
            conexao.close()