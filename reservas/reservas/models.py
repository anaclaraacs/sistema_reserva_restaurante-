from django.db import models
from django.forms import ValidationError
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password
import uuid


# Modelo Cliente
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=14)
    email = models.EmailField(max_length=255, unique=True)
    senha = models.CharField(max_length=255)

    def set_senha(self, senha):
        # Criptografa a senha antes de salvar
        self.senha = make_password(senha)

    def verificar_senha(self, senha):
        return check_password(senha, self.senha)


    def __str__(self):
        return self.nome

# Modelo Mesa
class Mesa(models.Model):
    numero = models.IntegerField(unique=True)
    capacidade = models.IntegerField()
    ocupada = models.BooleanField(default=False)

    def __str__(self):
        return f"Mesa {self.numero} - {self.capacidade} pessoas"


# Modelo Reserva


class Reserva(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
    ]

    id_reserva = models.CharField(max_length=36, unique=True, default=uuid.uuid4, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    data = models.DateField()  
    hora = models.TimeField()  #
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDENTE')
    email_cliente = models.EmailField(max_length=255, editable=False) 
    capacidade = models.IntegerField()
    pessoas = models.IntegerField()

    def clean(self):
        # Combinar data e hora apenas para validação
        data_hora_reserva = datetime.combine(self.data, self.hora)
        
        # Verificar conflitos de reserva
        if Reserva.objects.filter(
            mesa=self.mesa,
            data=self.data,
            hora=self.hora
        ).exclude(pk=self.pk).exists():
            raise ValidationError('Esta mesa já está reservada para o horário selecionado.')

        # Validar se a data e hora são futuras
        if data_hora_reserva <= datetime.now():
            raise ValidationError('A data e hora da reserva devem ser futuras.')

        # Configurar valores adicionais
        if hasattr(self.cliente, 'email'):
            self.email_cliente = self.cliente.email  # Adiciona o email do cliente se existir
        self.capacidade = self.mesa.capacidade  # Define a capacidade da mesa

    def __str__(self):
        return f"Reserva para {self.pessoas} pessoa(s) na Mesa {self.mesa} em {self.data} às {self.hora}"

    def __str__(self):
        return f"Reserva {self.id_reserva} de {self.cliente.nome} para a Mesa {self.mesa.numero} em {self.data.strftime('%d/%m/%Y')} às {self.hora.strftime('%H:%M')} - Status: {self.status}"

