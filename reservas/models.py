from django.db import models
from django.forms import ValidationError
from validate_docbr import CPF


# Função para validar CPF
def validar_cpf(value):
    cpf = CPF()
    if not cpf.validate(value):
        raise ValidationError('CPF inválido')


# Modelo Cliente
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, validators=[validar_cpf])
    telefone = models.CharField(max_length=14)

    def __str__(self):  # retorna o nome do cliente como uma string
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
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()


    def __str__(self):
        return f"Reserva de {self.cliente.nome} para a Mesa {self.mesa.numero} em {self.data_hora.strftime('%d/%m/%Y %H:%M')}"
