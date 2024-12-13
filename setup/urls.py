from django.contrib import admin
from django.urls import path
from reservas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('reserva/', views.fazer_reserva, name='reserva'),
    path('perfil/', views.perfil, name='perfil'),
    path('login/', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    # path('fazer_reserva/', views.fazer_reserva, name='fazer_reserva'),
]

