from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from .models import Mesa, Cliente, Reserva
from datetime import datetime
from django.core.exceptions import ValidationError
from .forms import Cadastro, Login

def home(request):
    return render(request, 'reservas/home.html') 

def reserva(request):
    return render(request, 'reservas/reserva.html')

def perfil(request):
    # Verifica se o cliente está logado
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('login')  # Redireciona para a página de login caso o cliente não esteja logado

    # Busca o cliente logado
    try:
        cliente = Cliente.objects.get(id=cliente_id)
    except Cliente.DoesNotExist:
        return HttpResponse("Cliente não encontrado.")
    
    return render(request, 'reservas/perfil.html', {'cliente': cliente})


def login(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']
            try:
                
                #verificar sequencia de messegens, estão acumulando ao fazer login e exibindo no cadastro
                cliente = Cliente.objects.get(email=email)
                if cliente.verificar_senha(senha):
                    request.session['cliente_id'] = cliente.id  # Salva o ID na sessão
                    messages.success(request, f"Bem-vindo, {cliente.nome}!")
                    return redirect('perfil')  # Redireciona para a página de perfil
                else:
                    messages.error(request, "Senha incorreta.")
            except Cliente.DoesNotExist:
                messages.error(request, "Email não encontrado.")
    else:
        form = Login()  # Cria o formulário vazio para o método GET

    return render(request, 'reservas/login.html', {'form': form})


def cadastro(request):
    if request.method == 'POST':
        form = Cadastro(request.POST)
        
        if form.is_valid():
            # Se o formulário for válido, salva o novo cliente
            form.save()
            login_url = reverse('login')
            messages.success(request, f"Cadastro realizado com sucesso! Faça login. <a href='{login_url}'>Clique aqui</a>.")
            return redirect('cadastro')
    else:
        form = Cadastro()

    return render(request, 'reservas/cadastro.html', {'form': form})

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
        return redirect('login')  # Substitua 'perfil' pela URL correspondente à página de perfil