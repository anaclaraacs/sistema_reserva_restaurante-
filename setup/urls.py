from django.contrib import admin
from django.urls import path
from reservas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('perfil/', views.perfil, name='perfil'),
    path('login/', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('fazer_reserva/', views.fazer_reserva, name='fazer_reserva'),
    path('excluir_reserva/', views.excluir_reserva, name='excluir_reserva'),
]

