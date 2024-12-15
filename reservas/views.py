from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from .models import Cliente, Reserva, Mesa
from .forms import Cadastro, Login
from django.core.exceptions import ValidationError

def home(request):
    return render(request, 'reservas/home.html') 

def perfil(request):
    # Verificar o cliente logado 
    cliente_id = request.session.get('cliente_id')  # Verifica o cliente na sessão
    if not cliente_id:
        return redirect('login')  # Se não houver cliente_id, redireciona para login

    # Busca o cliente logado
    try:
        cliente = Cliente.objects.get(id=cliente_id)
    except Cliente.DoesNotExist:
        return redirect('login')
    
    return render(request, 'reservas/perfil.html', {'cliente': cliente})


def login(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            cliente = form.cliente  
            request.session['cliente_id'] = cliente.id  # Armazena o cliente_id na sessão
            return redirect('perfil')  # Redireciona para o perfil após o login bem-sucedido
        else:
            # Caso o formulário não seja válido, exibe as mensagens de erro
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = Login()  

    return render(request, 'reservas/login.html', {'form': form})

def cadastro(request):
    if request.method == 'POST':
        form = Cadastro(request.POST)
        
        if form.is_valid():
            form.save()
            login_url = reverse('login')  # Obtem a URL correta para o login
            messages.success(request, f"Cadastro realizado com sucesso! Faça login. <a href='{login_url}'>Clique aqui</a>.")
    else:
        form = Cadastro()

    return render(request, 'reservas/cadastro.html', {'form': form})

def fazer_reserva(request):
    if request.method == 'POST':
        cliente_id = request.session.get('cliente_id')
        if not cliente_id:
            return redirect(reverse('login'))

        try:
            cliente = Cliente.objects.get(id=cliente_id)
        except Cliente.DoesNotExist:
            return HttpResponse("Cliente não encontrado.")
        
        # Coletar os dados do formulário
        mesa_id = request.POST.get('mesa')
        pessoas = request.POST.get('pessoas')
        data = request.POST.get('data')
        hora = request.POST.get('hora')
        
        # Obter a mesa selecionada
        try:
            mesa = Mesa.objects.get(id=mesa_id)
        except Mesa.DoesNotExist:
            return HttpResponse("Mesa não encontrada.")
        
        # Criar a reserva
        reserva = Reserva(
            cliente=cliente,
            mesa=mesa,
            data=data,
            hora=hora,
            pessoas=pessoas,
            email_cliente=cliente.email,
            capacidade=5,           
        )
        
        # Validar a reserva
        try:
            reserva.full_clean()  # Executa as validações no modelo
            reserva.save()
            return redirect('perfil')  # Redireciona para o perfil após salvar a reserva
        except ValidationError as e:
            return render(request, 'reservas/perfil.html', {'form': reserva, 'errors': e.message_dict})
    else:
        return render(request, 'reservas/reserva.html')
    
def excluir_reserva(request):
    if request.method == 'POST':
        numero_mesa = request.POST.get('numero_mesa')
        try:
            reserva = Reserva.objects.get(mesa=numero_mesa)
            reserva.delete()
            return HttpResponse("Reserva excluída com sucesso!")
        except Reserva.DoesNotExist:
            return HttpResponse("Reserva não encontrada para o número da mesa informado.")
    
    return redirect('reservas/perfil') 