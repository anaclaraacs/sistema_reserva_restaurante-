# Usar imagem oficial do Python
FROM python:3.10

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos para o contêiner
COPY . /app/

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expôr a porta do Django
EXPOSE 8000

# Comando para iniciar o Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]