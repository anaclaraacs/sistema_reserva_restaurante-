from django.db import models
from django.forms import ValidationError
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password


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


    def __str__(self):  # Retorna o nome do cliente como uma string
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

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDENTE')  
    
    def clean(self):
         #evitar reservas duplicadas para a mesma mesa no mesmo horário
        if Reserva.objects.filter(mesa=self.mesa, data_hora=self.data_hora).exclude(pk=self.pk).exists():
            raise ValidationError('Esta mesa já está reservada para o horário selecionado.')

        # Validação para garantir que a reserva seja feita para uma data futura
        if self.data_hora <= datetime.now():
            raise ValidationError('A data e hora da reserva devem ser futuras.')

    def save(self, *args, **kwargs):
        # Atualiza o status de ocupada da mesa ao confirmar a reserva
        if self.status == 'CONFIRMADA':
            self.mesa.ocupada = True
            self.mesa.save()
        elif self.status == 'CANCELADA':
            self.mesa.ocupada = False
            self.mesa.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva de {self.cliente.nome} para a Mesa {self.mesa.numero} em {self.data_hora.strftime('%d/%m/%Y %H:%M')} - Status: {self.status}"
