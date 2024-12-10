from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Mesa, Cliente, Reserva
from datetime import datetime
from django.core.exceptions import ValidationError


def home_view(request):
    return render(request, 'reservas/home.html') 

def reserva_view(request):
    return render(request, 'reservas/reserva.html')

def perfil_view(request):
    return render(request, 'reservas/perfil.html')

def login_view(request):
    return render(request, 'reservas/login.html')

def cadastro_view(request):
    return render(request, 'reservas/cadastro.html')


def fazer_reserva(request):
    # Verifica se o cliente está logado
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('login')  # Redireciona para a página de login caso o cliente não esteja logado
    
    # Busca o cliente logado
    try:
        cliente = Cliente.objects.get(id=cliente_id)
    except Cliente.DoesNotExist:
        return HttpResponse("Cliente não encontrado.")

    # Se for um POST (formulário enviado)
    if request.method == 'POST':
        # Obtém os dados do formulário
        mesa_id = request.POST.get('mesa')
        data_reserva = request.POST.get('data')
        hora_reserva = request.POST.get('hora')
        quantidade_pessoas = request.POST.get('pessoas')

        # Converte data e hora para o formato correto
        try:
            data_hora = datetime.strptime(f"{data_reserva} {hora_reserva}", "%Y-%m-%d %H:%M")
        except ValueError:
            return HttpResponse("Formato de data e hora inválido.")

        # Tenta obter a mesa do banco de dados
        try:
            mesa = Mesa.objects.get(id=mesa_id)
        except Mesa.DoesNotExist:
            return HttpResponse("Mesa não encontrada.")

        # Cria a reserva
        reserva = Reserva(cliente=cliente, mesa=mesa, data_hora=data_hora, status='PENDENTE')
        
        # Valida a reserva
        try:
            reserva.full_clean()  # Chama o método clean do modelo
        except ValidationError as e:
            return HttpResponse(str(e))  # Exibe o erro de validação, caso exista

        # Salva a reserva
        reserva.save()

        # Marca a mesa como ocupada
        mesa.ocupada = True
        mesa.save()

        # Redireciona para o perfil do cliente após a reserva
        return redirect('perfil')  # Substitua 'perfil' pela URL correspondente à página de perfil