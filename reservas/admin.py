from django.contrib import admin
from .models import Cliente, Mesa, Reserva


# @admin.register(Cliente)
# class ClienteAdmin(admin.ModelAdmin):
#     list_display = ('nome', 'cpf', 'telefone')  
#     search_fields = ('nome', 'cpf')  # Permite buscar por nome ou CPF

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone')  # Campos exibidos na lista
    search_fields = ('nome', 'email')            # Campos para busca


@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'capacidade', 'ocupada')  
    list_filter = ('ocupada',)  
    search_fields = ('numero',)  


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'mesa', 'data', 'hora', 'status')  
    list_filter = ('status', 'data', 'hora')  
    search_fields = ('cliente__nome', 'mesa__numero')  
