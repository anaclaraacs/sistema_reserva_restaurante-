from django.db import models
from django.forms import ValidationError
from validate_docbr import CPF


def validar_cpf(value):
    cpf = CPF()
    if not cpf.validate(value):
        raise ValidationError('Cpf inválido')

class Cliente(models.Model):
    nome=models.CharField(max_length=100)
    cpf=models.CharField(max_length=14,validators=[validar_cpf])
    telefone=models.CharField(max_length=14)


    def __str__(self):  # retorna o nome do cliente (representa o objeto como uma string)
        return self.nome 
    

class Mesa(models.Model):
    numero=models.IntegerField(unique=True)
    capacidade=models.IntegerField()
    ocupada=models.BooleanField(default=False)

    def __str__(self):
        return f"Mesa {self.numero} - {self.capacidade} pessoas"
     


