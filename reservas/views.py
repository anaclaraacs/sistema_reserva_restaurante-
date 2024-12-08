from django.shortcuts import render

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