from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Cliente, Mesa, Reserva

admin.site.register(Cliente)
admin.site.register(Mesa)
admin.site.register(Reserva)
