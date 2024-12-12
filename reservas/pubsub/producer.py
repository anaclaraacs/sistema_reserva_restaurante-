from confluent_kafka import Producer
import json

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

producer = Producer({'bootstrap.servers': 'localhost:9092'})

def publicar_reserva(reserva):
    # Converte os dados da reserva em JSON
    reserva_json = json.dumps(reserva)
    # Envia para o tópico
    producer.produce('criar-reserva', value=reserva_json, callback=delivery_report)
    producer.flush()

# Exemplo de uso
reserva = {
    "cliente_email": "cliente@example.com",
    "restaurante_telegram": "@restaurante",
    "data": "2024-12-15",
    "hora": "20:00"
}
publicar_reserva(reserva)