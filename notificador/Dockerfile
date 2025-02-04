# Usar a imagem base do Python
FROM python:3.9-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o arquivo requirements.txt para o container
#COPY requirements.txt /app/

# Instalar as dependências do projeto
#RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do serviço consumidor Kafka para o container
COPY . /app

# Definir o comando para rodar o consumidor Kafka
CMD ["python", "notificador_consumidor.py"]
