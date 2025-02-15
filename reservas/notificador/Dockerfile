FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir pika python-dotenv

CMD ["python", "notificador_consumidor.py"]