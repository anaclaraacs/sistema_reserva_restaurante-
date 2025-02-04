from confluent_kafka import Producer

KAFKA_BROKER = "kafka:9092"
TOPIC = "reservas"

# Configuração do produtor
producer_conf = {
    'bootstrap.servers': 'kafka:9092',
    'security.protocol': 'PLAINTEXT',  # Garante que não é usado SSL
    'acks': 'all',
}

producer = Producer(producer_conf)

def enviar_mensagem(reserva_id, cliente_email):
    mensagem = f"Reserva {reserva_id} confirmada para {cliente_email}"
    producer.produce(TOPIC, mensagem.encode("utf-8"))
    producer.flush()  # Garante que a mensagem foi enviada
    print(f"📩 Mensagem enviada para o Kafka: {mensagem}")

