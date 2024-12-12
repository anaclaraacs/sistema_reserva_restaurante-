from confluent_kafka import Consumer
import json
import smtplib  # Para envio de e-mails
import requests  # Para chamar a API do Telegram
import telegram

def enviar_email(event_data):
    try:
        cliente_email = event_data["cliente_email"]
        assunto = "Confirmação de Reserva"
        mensagem = f"Olá, sua reserva foi confirmada para o dia {event_data['data_reserva']}."
        
        # Configuração do envio de e-mail (SMTP)
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("seu_email@gmail.com", "sua_senha")
            server.sendmail(
                "seu_email@gmail.com",
                cliente_email,
                f"Subject: {assunto}\n\n{mensagem}"
            )
        print(f"E-mail enviado para {cliente_email}")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

def enviar_telegram(event_data):
    try:
        bot = telegram.Bot(token='SEU_TOKEN_DO_BOT')
        info = bot.getMe()
        bot_id = info.id
        mensagem = f"Nova reserva criada: {event_data['data_reserva']} para {event_data['cliente_email']}."
        
        # Chamada à API do Telegram
        url = f"https://api.telegram.org/bot7682475969:AAF4W4sRuHoBoyjxLGFwjBeykGDfgZkoERE/sendMessage"
        payload = {"chat_id": bot_id, "text": mensagem}
        requests.post(url, data=payload)
        print("Mensagem enviada para o Telegram")
    except Exception as e:
        print(f"Erro ao enviar mensagem no Telegram: {e}")

def start_consumer():
    consumer = Consumer({
        "bootstrap.servers": "localhost:9092",
        "group.id": "notificacao",
        "auto.offset.reset": "earliest"
    })
    consumer.subscribe(["criar-reserva"])

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Erro no consumidor: {msg.error()}")
            continue

        # Processar a mensagem
        event_data = json.loads(msg.value().decode("utf-8"))
        enviar_email(event_data)
        enviar_telegram(event_data)
