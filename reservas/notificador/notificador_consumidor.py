import pika
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import json
import os 
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = "localhost"
QUEUE_NAME = "reservas"

logging.basicConfig(
     level=logging.INFO,
     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
 )
logger = logging.getLogger(__name__)

# def callback(ch, method, properties, body):
#     mensagem = body.decode("utf-8")
#     logger.info(f"Mensagem recebida: {mensagem}")
#     # Aqui você pode adicionar a lógica para enviar notificações

# # Configuração do e-mail
SMTP_SERVER = "smtp.gmail.com" 
SMTP_PORT = 587
EMAIL_REMETENTE =  os.getenv("email")
EMAIL_SENHA = os.getenv("senha")  

def enviar_email(email_destinatario, mensagem):
    """Função para enviar um e-mail."""
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_REMETENTE
        msg["To"] = email_destinatario
        msg["Subject"] = "Confirmação de Reserva"

        msg.attach(MIMEText(mensagem, "plain"))

        # Conectando ao servidor SMTP
        servidor_smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        servidor_smtp.starttls()
        servidor_smtp.login(EMAIL_REMETENTE, EMAIL_SENHA)

        # Enviar o e-mail
        servidor_smtp.sendmail(EMAIL_REMETENTE, email_destinatario, msg.as_string())

        servidor_smtp.quit()
        logger.info(f"E-mail enviado para {email_destinatario}")
    
    except Exception as e:
        logger.error(f"Erro ao enviar e-mail: {e}")

def callback(ch, method, properties, body):
    """Função chamada ao receber uma mensagem na fila do RabbitMQ."""
    try:
        dados = json.loads(body.decode("utf-8"))  # Supondo que a mensagem seja um JSON
        email_cliente = dados.get("email_cliente")
        mesa = dados.get("mesa")

        logger.info(f"Mensagem recebida: {dados}")

        if email_cliente:
            mensagem_email = f"Olá! Sua reserva para a mesa {mesa} foi confirmada. Obrigado por escolher nosso restaurante!"
            enviar_email(email_cliente, mensagem_email)
    
    except Exception as e:
        logger.error(f"Erro no processamento da mensagem: {e}")

# Conexão com RabbitMQ
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

logger.info("Consumidor RabbitMQ rodando...")
canal.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)

canal.start_consuming()

