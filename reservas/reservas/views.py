from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from .models import Cliente, Reserva, Mesa
from .forms import Cadastro, Login
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime
from notificador.notificador_produtor import enviar_mensagem


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
    mesas_disponiveis = Mesa.objects.filter(ocupada=False)  # Só traz mesas livres
    if request.method == 'POST':
        cliente_id = request.session.get('cliente_id')
        if not cliente_id:
            return redirect(reverse('login'))

        try:
            cliente = Cliente.objects.get(id=cliente_id)
            cliente.save()
        except Cliente.DoesNotExist:
            login_url = reverse('login')
            messages.error(request,f"Cliente não encontrado. Faça login: <a href='{login_url}'>Clique aqui</a>.")

            return render(request, "reservas/reserva.html", {"mesas": mesas_disponiveis})

        
        # Coletar os dados do formulário
        mesa_id = request.POST.get('mesa')
        data = request.POST.get('data')
        hora = request.POST.get('hora')
        
       # Variáveis para data e hora
        data_reserva = None
        hora_reserva = None
        
        # Converter data e hora para validação
        try:
            data_reserva = datetime.strptime(data, '%Y-%m-%d').date()
            hora_reserva = int(hora.split(':')[0])  # Pega apenas a hora
        except ValueError:
            messages.error(request, "Formato de data ou hora inválido.")
            return render(request, "reservas/reserva.html", {"mesas": mesas_disponiveis})

        
        # Validar se a data é anterior ao dia atual
        if data_reserva < timezone.now().date():
            messages.error(request, "Não é possível reservar para dias anteriores ao atual.")
            return render(request, "reservas/reserva.html", {"mesas": mesas_disponiveis})
        
        # Validar se o horário está entre 18h e 23h
        if hora_reserva < 18 or hora_reserva > 23:
            messages.error(request, "O horário da reserva deve ser entre 18h e 23h.")
            return render(request, "reservas/reserva.html", {"mesas": mesas_disponiveis})

        
        # Obter a mesa selecionada
        try:
            mesa = Mesa.objects.get(id=mesa_id)
        except Mesa.DoesNotExist:
            messages.error(request, "Mesa não encontrada")
            return render(request, "reservas/reserva.html", {"mesas": mesas_disponiveis})
        
        #Verificar se a mesa está ocupada
        if mesa.ocupada == True:
            messages.error(request, "Esta mesa já está ocupada.")
            return render(request, "reservas/reserva.html", {"mesas": mesas_disponiveis})
 
        else:
            mesa.ocupada = True
            mesa.save()
        
        # Criar a reserva
        reserva = Reserva(
            cliente=cliente,
            mesa=mesa,
            data=data,
            hora=hora,
            email_cliente=cliente.email,
            capacidade=mesa.capacidade,        
        )
        
        # Validar a reserva
        try:
            reserva.full_clean()  # Executa as validações no modelo
            reserva.save()
            print(f"Cliente ID: {cliente_id}, Nome: {cliente.nome}, Email: {cliente.email}")

            enviar_mensagem(reserva.mesa.numero, reserva.email_cliente)
            
            return redirect('perfil')  # Redireciona para o perfil após salvar a reserva
        except ValidationError as e:
            return render(request, 'reservas/perfil.html', {'form': reserva, 'errors': e.message_dict})
    else:
        return render(request, "reservas/reserva.html", {"mesas": mesas_disponiveis})
    
def excluir_reserva(request):
    if request.method == 'POST':
        numero_mesa = request.POST.get('numero_mesa')
        
        cliente_id = request.session.get('cliente_id')  # Obtém o ID do cliente logado
        if not cliente_id:
            messages.error(request, "Você precisa estar logado para excluir uma reserva.")
            return redirect("login")

        try:
            cliente = Cliente.objects.get(id=cliente_id)  # Obtém o cliente logado
            mesa = Mesa.objects.get(numero=numero_mesa)
            reserva = Reserva.objects.get(mesa=mesa, cliente=cliente)  # Busca apenas reservas do cliente logado
            
            reserva.delete()

            # Liberar a mesa
            mesa.ocupada = False
            mesa.save()
            
            messages.success(request, "Reserva excluída com sucesso!")

            # Atualizar a lista de reservas do cliente
            reservas = Reserva.objects.filter(cliente=cliente)
            return render(request, "reservas/perfil.html", {"cliente": cliente, "reservas": reservas})

        except Cliente.DoesNotExist:
            messages.error(request, "Cliente não encontrado.")
            return redirect("login")
        except Mesa.DoesNotExist:
            messages.error(request, "Mesa não encontrada.")
            return redirect("perfil")
        except Reserva.DoesNotExist:
            messages.error(request, "Reserva não encontrada para a mesa informada.")
            return redirect("perfil")

    return redirect('perfil')
