#!/bin/bash
echo "Aguardando Kafka..."
while ! nc -z kafka 9092; do
  sleep 2
done
echo "Kafka está pronto! Iniciando Django..."
exec "$@"
