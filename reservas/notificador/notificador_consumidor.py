import pika
import json
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configurações do RabbitMQ
RABBITMQ_HOST = "rabbitmq"  
QUEUE_NAME = "reservas"

# Configurações do SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_REMETENTE = "julianaferris2024@gmail.com"  
EMAIL_SENHA = "aleo urum xomi ipza"  

def enviar_email(email_destinatario, mensagem):
    """Função para enviar um e-mail."""
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_REMETENTE
        msg["To"] = email_destinatario
        msg["Subject"] = "Confirmação de Reserva"
        msg.attach(MIMEText(mensagem, "plain"))

        servidor_smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        servidor_smtp.starttls()
        servidor_smtp.login(EMAIL_REMETENTE, EMAIL_SENHA)
        servidor_smtp.sendmail(EMAIL_REMETENTE, email_destinatario, msg.as_string())
        servidor_smtp.quit()
        logger.info(f"E-mail enviado para {email_destinatario}")
    except Exception as e:
        logger.error(f"Erro ao enviar e-mail: {e}")

def callback(ch, method, properties, body):
    """Função chamada ao receber uma mensagem na fila do RabbitMQ."""
    try:
        logger.info(f"Recebido: {body.decode('utf-8')}")
        dados = json.loads(body.decode("utf-8"))
        email_cliente = dados.get("email_cliente")
        mesa_id = dados.get("mesa_id")

        logger.info(f"Processando reserva para o e-mail: {email_cliente}, mesa: {mesa_id}")

        if email_cliente and mesa_id:
            mensagem_email = f"Olá! Sua reserva para a mesa {mesa_id} foi confirmada. Obrigado por escolher nosso restaurante!"
            enviar_email(email_cliente, mensagem_email)
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {e}")

# Conexão com RabbitMQ
while True:
    try:
        conexao = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        canal = conexao.channel()
        canal.queue_declare(queue=QUEUE_NAME)
        logger.info("Conectado ao RabbitMQ com sucesso.")
        canal.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
        canal.start_consuming()
    except Exception as e:
        logger.error(f"Erro na conexão com RabbitMQ: {e}. Tentando reconectar em 5 segundos...")
        time.sleep(5)