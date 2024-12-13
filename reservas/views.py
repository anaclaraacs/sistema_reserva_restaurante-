from django.shortcuts import render, redirect,  get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from .models import Cliente, Reserva, Mesa
from .forms import Cadastro, Login
from django.contrib.auth.decorators import login_required

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
            return redirect('perfil')
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
            # Se o formulário for válido, salva o novo cliente
            form.save()
            login_url = reverse('login')
            messages.success(request, f"Cadastro realizado com sucesso! Faça login. <a href='{login_url}'>Clique aqui</a>.")
            return redirect('cadastro')
    else:
        form = Cadastro()

    return render(request, 'reservas/cadastro.html', {'form': form})

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Mesa, Cliente, Reserva

@login_required
def fazer_reserva(request):
    if request.method == 'POST':
        mesa_numero = request.POST.get('mesa_numero')
        mesa_capacidade = request.POST.get('pessoas')
        data = request.POST.get('data')
        hora = request.POST.get('hora')
        pessoas = request.POST.get('pessoas')

        # Captura o email diretamente do objeto request.user, se o usuário estiver logado
        email_cliente = request.user.email  # Usando o email do usuário autenticado
        
        if not email_cliente:
            return HttpResponse("Você precisa estar logado para fazer uma reserva.", status=403)

        try:
            cliente = Cliente.objects.get(email=email_cliente)
        except Cliente.DoesNotExist:
            return HttpResponse("Cliente não encontrado!", status=404)

        mesa, created = Mesa.objects.get_or_create(
            numero=mesa_numero,
            defaults={'capacidade': mesa_capacidade, 'ocupada': False}
        )

        reserva = Reserva.objects.create(
            cliente=cliente,
            mesa=mesa,
            data=data,
            hora=hora,
            pessoas=pessoas,
            capacidade=mesa.capacidade,
            email_cliente=cliente.email,
        )

        mesa.ocupada = True
        mesa.save()

        return HttpResponse(f"Reserva criada com sucesso: {reserva.id_reserva}")

    return render(request, 'reservas/reserva.html')

    
    
    
    
    
    
    
    
    # Verifica se o cliente está logado
    # cliente_id = request.session.get('cliente_id')
    # if not cliente_id:
    #     messages.error(request, "Você precisa estar logado para fazer uma reserva.")
    #     return redirect('login')  # Redireciona para a página de login
    
    # Busca o cliente logado
    # cliente = get_object_or_404(Cliente, id=cliente_id)

    # Busca todas as mesas disponíveis
    # mesas = Mesa.objects.all()

    # if request.method == "POST":
    #     form = FazerReserva(request.POST)
    #     if form.is_valid():
    #         Obtém os dados validados do formulário
    #         mesa_id = form.cleaned_data['mesa']
    #         data_reserva = form.cleaned_data['data']
    #         hora_reserva = form.cleaned_data['hora']
    #         quantidade_pessoas = form.cleaned_data['pessoas']

    #         Converte data e hora para o formato correto
    #         data_hora = datetime.combine(data_reserva, hora_reserva)

    #         Verifica se a mesa está disponível
    #         mesa = get_object_or_404(Mesa, id=mesa_id)
    #         if Reserva.objects.filter(mesa=mesa, data=data_reserva, hora=hora_reserva).exists():
    #             messages.error(request, f"A Mesa {mesa.numero} já está reservada para esse horário.")
    #             return redirect('fazer_reserva')

    #         Verifica capacidade da mesa
    #         if quantidade_pessoas > mesa.capacidade:
    #             messages.error(request, f"A Mesa {mesa.numero} suporta no máximo {mesa.capacidade} pessoas.")
    #             return redirect('fazer_reserva')

    #         Cria e salva a reserva
    #         reserva = Reserva(cliente=cliente, mesa=mesa, data=data_reserva, hora=hora_reserva, pessoas=quantidade_pessoas)
    #         reserva.save()

    #         Marca a mesa como ocupada (opcional, dependendo da lógica)
    #         mesa.ocupada = True
    #         mesa.save()

    #         Mensagem de sucesso
    #         messages.success(request, f"Reserva realizada com sucesso! Mesa {mesa.numero}, {data_reserva} às {hora_reserva}.")
    #         return redirect('sucesso')
    #     else:
    #         Exibe erros do formulário
    #         for error in form.errors.values():
    #             messages.error(request, error)

    # else:
    #     form = FazerReserva()

    # return render(request, 'reservas/reserva.html', {'form': form, 'mesas': mesas})
