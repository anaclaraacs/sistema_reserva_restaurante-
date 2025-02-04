from confluent_kafka import Consumer

KAFKA_BROKER = "kafka:9092"
TOPIC = "reservas"

# Configuração do consumidor
consumer_conf = {
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'grupo_notificador',
    'auto.offset.reset': 'earliest'  # Começa a consumir do início do tópico
}

consumer = Consumer(consumer_conf)
consumer.subscribe([TOPIC])

print("🎧 Consumidor Kafka rodando...")

while True:
    mensagem = consumer.poll(1.0)  # Espera 1 segundo por novas mensagens

    if mensagem is None:
        continue
    if mensagem.error():
        print(f"❌ Erro: {mensagem.error()}")
        continue

    print(f"📩 Mensagem recebida: {mensagem.value().decode('utf-8')}")
