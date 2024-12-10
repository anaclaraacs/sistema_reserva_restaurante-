from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import FormEmail

def home(request):
    return render(request, 'reservas/home.html') 

def reserva(request):
    return render(request, 'reservas/reserva.html')

def perfil(request):
    return render(request, 'reservas/perfil.html')

def login(request):
    return render(request, 'reservas/login.html')

def cadastro(request):
    if request.method == 'POST':
        form = FormEmail(request.POST) #altera a autenticação nativa do python para email
        if form.is_valid():
            email = form.cleaned_data['username'] 
            password = form.cleaned_data['password'] #aqui ele vai verificar a senha dentro dos dados que ja foram validados
            user = authenticate(request, username=email, password=password) #A funçaõ verifica se possui esses dados 
            #Aqui vai verificar se o usuaru
            if user is not None: 
                login(request, user)
                return redirect('perfil')  # Redireciona para a página principal após o login
            else:
                form.add_error(None, 'Credenciais inválidas')
    else:
        form = EmailAuthenticationForm()

    return render(request, 'login.html', {'form': form})

    return render(request, 'reservas/cadastro.html')